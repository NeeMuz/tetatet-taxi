"""Статусы заказа и проверки активной поездки."""
from .models import Order

ACTIVE_ORDER_STATUSES = ('new', 'accepted', 'arrived', 'on_way')

PASSENGER_CANCEL_STATUSES = frozenset({'new', 'accepted', 'arrived'})


def get_active_order(user):
    if not user or not user.is_authenticated:
        return None
    return (
        Order.objects.filter(user=user, status__in=ACTIVE_ORDER_STATUSES)
        .order_by('-created_at')
        .first()
    )
