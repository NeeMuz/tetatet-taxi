from django.urls import path

from .views import (
    dispatcher_login_view,
    dispatcher_page,
    home_view,
    landing_view,
    login_view,
    logout_view,
    order_history,
    order_page,
    order_track,
    password_view,
    profile_view,
    register_view,
    set_language_view,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('order/', order_page, name='order'),
    path('orders/', order_history, name='order_history'),
    path('orders/<int:pk>/', order_track, name='order_track'),
    path('profile/', profile_view, name='profile'),
    path('profile/password/', password_view, name='password'),
    path('set-language/', set_language_view, name='set_language'),
    path('dispatcher/login/', dispatcher_login_view, name='dispatcher_login'),
    path('dispatcher/', dispatcher_page, name='dispatcher'),
    path('', landing_view, name='landing'),
]
