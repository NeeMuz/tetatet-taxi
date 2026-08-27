from django.urls import path

from .views import DispatchOrderListView, OrderDetailView, OrderListCreateView

urlpatterns = [
    path('dispatch/orders/', DispatchOrderListView.as_view(), name='dispatch_orders'),
    path('orders/', OrderListCreateView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
]
