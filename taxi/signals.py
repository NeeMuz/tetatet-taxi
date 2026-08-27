from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order
from .services import broadcast_order_event


@receiver(post_save, sender=Order)
def notify_order_change(sender, instance, created, **kwargs):
    event_type = 'order_created' if created else 'order_updated'
    broadcast_order_event(instance, event_type)
