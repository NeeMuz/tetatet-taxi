from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .serializers import OrderSerializer

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all().order_by("-created_at")
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

        return order

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            order = serializer.save()

            return Response({
                "id": order.id,
                "status": order.status,
                "created_at": order.created_at
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
