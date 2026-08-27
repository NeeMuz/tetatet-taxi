from tetatet.i18n_helpers import tariff_label

from .driver_profiles import get_driver_profile
from .models import Order


def serialize_dispatch_order(order, lang='ru'):
    profile = get_driver_profile(order.driver_name)
    return {
        'id': order.id,
        'status': order.status,
        'name': order.name,
        'phone': order.phone,
        'from_address': order.from_address,
        'to_address': order.to_address,
        'tariff': order.tariff,
        'tariff_display': tariff_label(order.tariff, lang),
        'driver_name': order.driver_name or '',
        'driver_rating': profile.get('rating', 4.8),
        'driver_car': profile.get('car', ''),
        'driver_plate': profile.get('plate', ''),
        'estimated_price': str(order.estimated_price),
        'created_at': order.created_at.strftime('%d.%m %H:%M'),
    }


def dispatch_orders_queryset():
    return Order.objects.select_related('user').order_by('-created_at')


def count_orders_by_status(orders):
    statuses = ['new', 'accepted', 'arrived', 'on_way', 'done', 'cancelled']
    counts = {s: 0 for s in statuses}
    for order in orders:
        if order.status in counts:
            counts[order.status] += 1
    return counts


def user_can_access_dispatch_api(user, request):
    """Диспетчер с правами — доступ к API заказов."""
    return user.is_authenticated and getattr(user, 'can_dispatch', False)
