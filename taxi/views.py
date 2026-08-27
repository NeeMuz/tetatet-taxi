from rest_framework import generics, status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from tetatet.translations import resolve_language, translate

from accounts.modes import is_dispatcher_mode

from .dispatch_helpers import dispatch_orders_queryset, serialize_dispatch_order, user_can_access_dispatch_api
from .models import Order
from .serializers import OrderDispatchSerializer, OrderSerializer, PassengerOrderUpdateSerializer


class IsDispatcherMode(BasePermission):
    def has_permission(self, request, view):
        return user_can_access_dispatch_api(request.user, request)


class DispatchOrderListView(generics.ListAPIView):
    """Все заказы для диспетчерской — синхронно с админкой."""

    permission_classes = [IsDispatcherMode]

    def get_queryset(self):
        return dispatch_orders_queryset()

    def list(self, request, *args, **kwargs):
        lang = resolve_language(request)
        orders = self.get_queryset()
        return Response([serialize_dispatch_order(o, lang) for o in orders])


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.select_related('user', 'payment_card').order_by('-created_at')
        if self.request.user.can_dispatch and is_dispatcher_mode(self.request):
            return queryset
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


class OrderDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.select_related('user', 'payment_card')
        if self.request.user.can_dispatch and is_dispatcher_mode(self.request):
            return queryset
        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            if self.request.user.can_dispatch and is_dispatcher_mode(self.request):
                return OrderDispatchSerializer
            return PassengerOrderUpdateSerializer
        return OrderSerializer

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        is_dispatch = request.user.can_dispatch and is_dispatcher_mode(request)

        if is_dispatch:
            return super().update(request, *args, **kwargs)

        if order.user_id != request.user.id:
            return Response({'detail': translate('api.no_access', resolve_language(request))}, status=status.HTTP_403_FORBIDDEN)

        serializer = PassengerOrderUpdateSerializer(
            data=request.data,
            context={'order': order},
        )
        serializer.is_valid(raise_exception=True)

        if 'trip_rating' in serializer.validated_data:
            order.trip_rating = serializer.validated_data['trip_rating']
            order.save(update_fields=['trip_rating', 'updated_at'])
        else:
            order.status = serializer.validated_data['status']
            order.save(update_fields=['status', 'updated_at'])

        return Response(OrderSerializer(order, context={'request': request}).data)
