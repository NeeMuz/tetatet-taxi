from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "orders",
            {
                "type": "order_created",
                "text": json.dumps({
                    "id": order.id,
                    "status": order.status,
                    "name": order.name,
                })
            }
        )
