from rest_framework import serializers

from accounts.models import PaymentCard
from tetatet.i18n_helpers import status_label, tariff_label
from tetatet.translations import resolve_language, translate

from .driver_profiles import get_driver_profile
from .models import Order
from .order_flow import get_active_order
from .services import can_transition, estimate_price


def _lang(serializer) -> str:
    request = serializer.context.get('request')
    return resolve_language(request) if request else 'ru'


def _t(serializer, key: str, **kwargs) -> str:
    msg = translate(key, _lang(serializer))
    return msg.format(**kwargs) if kwargs else msg


class OrderSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    tariff_display = serializers.SerializerMethodField()
    payment_card_id = serializers.PrimaryKeyRelatedField(
        queryset=PaymentCard.objects.all(),
        source='payment_card',
        required=False,
        allow_null=True,
        write_only=True,
    )
    payment_card_label = serializers.CharField(source='payment_card.display_label', read_only=True)
    driver_rating = serializers.SerializerMethodField()
    driver_car = serializers.SerializerMethodField()
    driver_plate = serializers.SerializerMethodField()

    def get_status_display(self, obj):
        return status_label(obj.status, _lang(self))

    def get_tariff_display(self, obj):
        return tariff_label(obj.tariff, _lang(self))

    def get_driver_rating(self, obj):
        return float(get_driver_profile(obj.driver_name).get('rating', 4.8))

    def get_driver_car(self, obj):
        return get_driver_profile(obj.driver_name).get('car', '')

    def get_driver_plate(self, obj):
        return get_driver_profile(obj.driver_name).get('plate', '')

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'name',
            'phone',
            'from_address',
            'to_address',
            'comment',
            'driver_note',
            'driver_name',
            'driver_rating',
            'driver_car',
            'driver_plate',
            'tariff',
            'tariff_display',
            'distance_km',
            'estimated_price',
            'status',
            'status_display',
            'payment_type',
            'payment_card_id',
            'payment_card_label',
            'trip_rating',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 'user', 'estimated_price', 'status',
            'driver_name', 'driver_rating', 'driver_car', 'driver_plate',
            'payment_card_label', 'trip_rating', 'created_at', 'updated_at',
        ]

    def validate_phone(self, value):
        phone = (value or '').strip()
        if not phone:
            raise serializers.ValidationError(_t(self, 'api.phone_required'))
        if len(phone) > 32:
            raise serializers.ValidationError(_t(self, 'api.phone_too_long'))
        return phone

    def validate_from_address(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(_t(self, 'api.from_required'))
        return value.strip()[:255]

    def validate_to_address(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(_t(self, 'api.to_required'))
        return value.strip()[:255]

    def validate_payment_card_id(self, card):
        request = self.context.get('request')
        if card and request and card.user_id != request.user.id:
            raise serializers.ValidationError(_t(self, 'api.card_not_yours'))
        return card

    def validate(self, data):
        request = self.context.get('request')
        if request and request.user.is_authenticated and get_active_order(request.user):
            raise serializers.ValidationError(_t(self, 'api.active_order'))

        payment_type = data.get('payment_type', 'cash')
        card = data.get('payment_card')
        if payment_type == 'card' and not card:
            raise serializers.ValidationError({'payment_card_id': _t(self, 'api.card_required')})
        if payment_type == 'cash':
            data['payment_card'] = None
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
            if not validated_data.get('phone'):
                validated_data['phone'] = request.user.phone
            name = (validated_data.get('name') or '').strip()
            if not name:
                validated_data['name'] = request.user.get_full_name().strip() or request.user.email

        validated_data['estimated_price'] = estimate_price(
            validated_data['from_address'],
            validated_data['to_address'],
            distance_km=validated_data.get('distance_km'),
            tariff=validated_data.get('tariff', 'economy'),
        )
        return super().create(validated_data)


class OrderDispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', 'driver_name', 'driver_note']

    def validate(self, data):
        instance = self.instance
        new_status = data.get('status', instance.status)

        if new_status != instance.status and not can_transition(instance.status, new_status):
            raise serializers.ValidationError({
                'status': _t(
                    self,
                    'api.status_transition',
                    **{'from': status_label(instance.status, _lang(self))},
                ),
            })

        if new_status == 'accepted' and not data.get('driver_name', instance.driver_name):
            raise serializers.ValidationError({
                'driver_name': _t(self, 'api.driver_required'),
            })

        return data

    def validate_status(self, value):
        if value not in dict(Order.STATUS_CHOICES):
            raise serializers.ValidationError(_t(self, 'api.status_invalid'))
        return value


class PassengerOrderUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['cancelled', 'on_way', 'done'], required=False)
    trip_rating = serializers.IntegerField(min_value=1, max_value=5, required=False)

    def validate(self, data):
        order = self.context['order']
        has_status = 'status' in data
        has_rating = 'trip_rating' in data

        if not has_status and not has_rating:
            raise serializers.ValidationError(_t(self, 'api.action_required'))

        if has_status and has_rating:
            raise serializers.ValidationError(_t(self, 'api.one_action'))

        if has_rating:
            if order.status != 'done':
                raise serializers.ValidationError({'trip_rating': _t(self, 'api.rating_done_only')})
            if order.trip_rating:
                raise serializers.ValidationError({'trip_rating': _t(self, 'api.rating_already')})
            return data

        value = data['status']
        if not can_transition(order.status, value):
            raise serializers.ValidationError({
                'status': _t(
                    self,
                    'api.status_transition',
                    **{'from': status_label(order.status, _lang(self))},
                ),
            })
        if value == 'on_way' and order.status != 'arrived':
            raise serializers.ValidationError({
                'status': _t(self, 'api.board_arrived_only'),
            })
        if value == 'done' and order.status != 'on_way':
            raise serializers.ValidationError({
                'status': _t(self, 'api.complete_on_way_only'),
            })
        return data
