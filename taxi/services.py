import json
from decimal import Decimal

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Цены в USD
BASE_FARE = Decimal('3.50')
PER_KM = Decimal('1.25')
FALLBACK_RATE = Decimal('0.50')
CURRENCY = 'USD'

from .tariffs import TARIFF_MULTIPLIERS

STATUS_TRANSITIONS = {
    'new': {'accepted', 'cancelled'},
    'accepted': {'arrived', 'cancelled'},
    'arrived': {'on_way', 'cancelled'},
    'on_way': {'done', 'cancelled'},
    'done': set(),
    'cancelled': set(),
}


def can_transition(current: str, new: str) -> bool:
    return new in STATUS_TRANSITIONS.get(current, set())


def estimate_price(
    from_address: str,
    to_address: str,
    distance_km: Decimal | float | None = None,
    tariff: str = 'economy',
) -> Decimal:
    multiplier = TARIFF_MULTIPLIERS.get(tariff, Decimal('1.00'))

    if distance_km is not None:
        base = BASE_FARE + PER_KM * Decimal(str(distance_km))
    else:
        route_units = max(len(from_address.strip()), len(to_address.strip())) / 10
        base = BASE_FARE + FALLBACK_RATE * Decimal(str(route_units))

    return (base * multiplier).quantize(Decimal('0.01'))


def broadcast_order_event(order, event_type: str) -> None:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    payload = {
        'type': event_type,
        'text': json.dumps({
            'event': event_type,
            'id': order.id,
            'status': order.status,
            'name': order.name,
            'phone': order.phone,
            'driver_name': order.driver_name,
            'estimated_price': str(order.estimated_price),
            'from_address': order.from_address,
            'to_address': order.to_address,
            'tariff': order.tariff,
            'tariff_display': order.get_tariff_display(),
            'created_at': order.created_at.isoformat(),
            'updated_at': order.updated_at.isoformat(),
        }),
    }
    async_to_sync(channel_layer.group_send)('orders', payload)
