from django.urls import path
from .views import register_view, login_view, logout_view, order_view
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('order/', login_required(order_view), name='order'),
]
