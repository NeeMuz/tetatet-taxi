from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from taxi.models import Order

from .models import User


def register_view(request):
    error = None

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone', '').strip()

        if User.objects.filter(username=email).exists():
            error = 'Пользователь с таким email уже существует'
        elif not phone:
            error = 'Укажите номер телефона'
        else:
            User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
            )
            return redirect('login')

    return render(request, 'register.html', {'error': error})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('order')

    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('order')
        else:
            error = 'Неверный email или пароль'

    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('landing')


def landing_view(request):
    if request.user.is_authenticated:
        return redirect('order')
    return render(request, 'landing.html')


@login_required
def profile_view(request):
    success = None
    error = None
    user = request.user

    if request.method == 'POST' and request.POST.get('form') == 'profile':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not first_name or not email:
            error = 'Имя и email обязательны'
        elif not phone:
            error = 'Номер телефона обязателен для заказа такси'
        elif User.objects.filter(username=email).exclude(pk=user.pk).exists():
            error = 'Этот email уже занят'
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = email
            user.phone = phone
            if request.FILES.get('avatar'):
                user.avatar = request.FILES['avatar']
            user.save()
            success = 'Профиль сохранён'

    return render(request, 'profile.html', {
        'success': success,
        'error': error,
        'needs_phone': not user.has_phone,
    })


@login_required
def password_view(request):
    success = None
    error = None

    if request.method == 'POST':
        current = request.POST.get('current_password', '')
        new_pass = request.POST.get('new_password', '')
        new_pass2 = request.POST.get('new_password2', '')

        if not request.user.check_password(current):
            error = 'Неверный текущий пароль'
        elif not new_pass:
            error = 'Введите новый пароль'
        elif new_pass != new_pass2:
            error = 'Пароли не совпадают'
        else:
            request.user.set_password(new_pass)
            request.user.save()
            update_session_auth_hash(request, request.user)
            success = 'Пароль изменён'

    return render(request, 'password.html', {'success': success, 'error': error})


@login_required
def order_page(request):
    return render(request, 'order.html', {
        'needs_phone': not request.user.has_phone,
        'user_phone': request.user.phone,
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})


def staff_required(view):
    return user_passes_test(lambda u: u.is_staff)(view)


@login_required
@staff_required
def dispatcher_page(request):
    orders = Order.objects.select_related('user').order_by('-created_at')
    context = {
        'orders': orders,
        'orders_new': orders.filter(status='new'),
        'orders_active': orders.filter(status__in=['accepted', 'on_way']),
        'orders_done': orders.filter(status='done'),
        'orders_cancelled': orders.filter(status='cancelled'),
        'drivers': ['Klaus M.', 'Anna S.', 'Thomas B.', 'Maria K.', 'Stefan R.'],
    }
    return render(request, 'dispatcher.html', context)
