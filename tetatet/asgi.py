import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from taxi.consumers import OrderConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tetatet.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter([
        path("ws/orders/", OrderConsumer.as_asgi()),
    ]),
})
