from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

import json
import re

from tetatet.translations import LANGUAGE_CODES, resolve_language, translate
from tetatet.i18n_helpers import translated_tariff_catalog

from taxi.driver_profiles import DRIVER_PROFILES, get_driver_profile
from taxi.models import Order
from taxi.order_flow import ACTIVE_ORDER_STATUSES, get_active_order
from taxi.tariffs import TARIFF_CATALOG, SPECIAL_TARIFFS, STANDARD_TARIFFS
from taxi.dispatch_helpers import (
    count_orders_by_status,
    dispatch_orders_queryset,
    serialize_dispatch_order,
)

from .modes import (
    DISPATCHER_MODE,
    PASSENGER_MODE,
    clear_app_mode,
    is_dispatcher_mode,
    is_passenger_mode,
    set_app_mode,
)
from .models import PaymentCard, User


def tr(request, key):
    return translate(key, resolve_language(request))


def apply_user_language(request, user):
    lang = getattr(user, 'preferred_language', None)
    if lang in LANGUAGE_CODES:
        request.session['language'] = lang


@require_POST
def set_language_view(request):
    lang = request.POST.get('language', 'ru')
    if lang not in LANGUAGE_CODES:
        lang = 'ru'
    request.session['language'] = lang
    if request.user.is_authenticated:
        User.objects.filter(pk=request.user.pk).update(preferred_language=lang)
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)


def sanitize_holder_name(name):
    cleaned = re.sub(r"[^a-zA-Zа-яА-ЯёЁ\s\-']", '', name or '').strip()
    return cleaned.upper()


def detect_card_brand(number: str) -> str:
    digits = ''.join(c for c in number if c.isdigit())
    if digits.startswith('4'):
        return 'visa'
    if digits and digits[0] in '25':
        return 'mastercard'
    return 'other'


def authenticate_by_email(request, email, password, prefer_dispatch=False):
    """Вход по email — ищет пользователя по email, проверяет пароль по username."""
    email = (email or '').strip()
    if not email or not password:
        return None

    by_email = User.objects.filter(email__iexact=email)
    by_username = User.objects.filter(username__iexact=email)
    candidates = (by_email | by_username).distinct()

    if not candidates.exists():
        return None

    if prefer_dispatch:
        user_obj = (
            candidates.filter(is_superuser=True).first()
            or candidates.filter(is_dispatcher=True).first()
            or candidates.first()
        )
    else:
        user_obj = (
            candidates.filter(is_dispatcher=False, is_superuser=False).first()
            or candidates.first()
        )

    return authenticate(request, username=user_obj.username, password=password)


def register_view(request):
    error = None

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        phone = request.POST.get('phone', '').strip()

        if not phone:
            error = tr(request, 'msg.register.phone_required')
        elif len(''.join(c for c in phone if c.isdigit())) > 15:
            error = tr(request, 'msg.register.phone_too_long')
        elif User.objects.filter(username=email).exists():
            error = tr(request, 'msg.register.email_exists')
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
    if request.user.is_authenticated and is_passenger_mode(request):
        return redirect('home')

    error = None
    info = None

    if request.user.is_authenticated and is_dispatcher_mode(request):
        info = tr(request, 'msg.login.dispatcher_info')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate_by_email(request, email, password)

        if user is not None:
            login(request, user)
            apply_user_language(request, user)
            set_app_mode(request, PASSENGER_MODE)
            return redirect('home')
        else:
            error = tr(request, 'msg.login.invalid')

    return render(request, 'login.html', {'error': error, 'info': info})


def dispatcher_login_view(request):
    if (
        request.user.is_authenticated
        and is_dispatcher_mode(request)
        and request.user.can_dispatch
    ):
        return redirect('dispatcher')

    error = None
    info = None

    if request.user.is_authenticated and is_passenger_mode(request):
        info = tr(request, 'msg.dispatcher.passenger_info')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = authenticate_by_email(request, email, password, prefer_dispatch=True)

        if user is None:
            error = tr(request, 'msg.login.invalid')
        elif not user.can_dispatch:
            error = tr(request, 'msg.dispatcher.no_access')
        else:
            login(request, user)
            apply_user_language(request, user)
            set_app_mode(request, DISPATCHER_MODE)
            return redirect('dispatcher')

    return render(request, 'dispatcher_login.html', {'error': error, 'info': info})


def logout_view(request):
    to_dispatcher = request.GET.get('from') == 'dispatcher'
    logout(request)
    clear_app_mode(request)
    if to_dispatcher:
        return redirect('dispatcher_login')
    return redirect('landing')


@never_cache
def landing_view(request):
    """Главная всегда остаётся главной — без редиректов."""
    return render(request, 'landing.html', {
        'passenger_mode': is_passenger_mode(request),
        'dispatcher_mode': is_dispatcher_mode(request),
    })


@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form_type = request.POST.get('form', 'profile')
        payments_forms = {'add_card', 'edit_card', 'delete_card', 'default_card'}
        anchor = 'payments' if form_type in payments_forms else 'profile'

        if form_type == 'add_card':
            number = request.POST.get('card_number', '').replace(' ', '')
            expiry_raw = request.POST.get('card_expiry', '').replace(' ', '')
            cvv = request.POST.get('card_cvv', '').strip()
            holder = sanitize_holder_name(request.POST.get('holder_name', ''))

            exp_month = ''
            exp_year = ''
            if '/' in expiry_raw:
                parts = expiry_raw.split('/')
                exp_month = parts[0].strip()
                exp_year = parts[1].strip()
                if len(exp_year) == 2:
                    exp_year = '20' + exp_year

            if len(number) < 13:
                messages.error(request, tr(request, 'msg.card.full_number'), extra_tags='payments')
            elif not exp_month.isdigit() or not exp_year.isdigit():
                messages.error(request, tr(request, 'msg.card.expiry'), extra_tags='payments')
            elif not (1 <= int(exp_month) <= 12):
                messages.error(request, tr(request, 'msg.card.month'), extra_tags='payments')
            elif len(cvv) != 3 or not cvv.isdigit():
                messages.error(request, tr(request, 'msg.card.cvv'), extra_tags='payments')
            else:
                brand = detect_card_brand(number)
                is_first = not user.payment_cards.exists()
                PaymentCard.objects.create(
                    user=user,
                    brand=brand,
                    pan=number,
                    last4=number[-4:],
                    exp_month=int(exp_month),
                    exp_year=int(exp_year),
                    holder_name=holder or sanitize_holder_name(user.get_full_name()),
                    cvv=cvv,
                    is_default=is_first or request.POST.get('set_default') == '1',
                )
                messages.success(request, tr(request, 'msg.card.saved'), extra_tags='payments')

        elif form_type == 'edit_card':
            card = PaymentCard.objects.filter(user=user, pk=request.POST.get('card_id')).first()
            if not card:
                messages.error(request, tr(request, 'msg.card.not_found'), extra_tags='payments')
            else:
                number_digits = ''.join(c for c in request.POST.get('card_number', '') if c.isdigit())
                expiry_raw = request.POST.get('card_expiry', '').replace(' ', '')
                cvv = request.POST.get('card_cvv', '').strip()
                holder = sanitize_holder_name(request.POST.get('holder_name', ''))
                brand = detect_card_brand(number_digits or card.pan)

                exp_month = ''
                exp_year = ''
                if '/' in expiry_raw:
                    parts = expiry_raw.split('/')
                    exp_month = parts[0].strip()
                    exp_year = parts[1].strip()
                    if len(exp_year) == 2:
                        exp_year = '20' + exp_year

                number_changed = bool(number_digits) and number_digits != card.pan

                if not exp_month.isdigit() or not exp_year.isdigit():
                    messages.error(request, tr(request, 'msg.card.expiry'), extra_tags='payments')
                elif not (1 <= int(exp_month) <= 12):
                    messages.error(request, tr(request, 'msg.card.month'), extra_tags='payments')
                elif brand not in dict(PaymentCard.BRAND_CHOICES):
                    messages.error(request, tr(request, 'msg.card.brand_invalid'), extra_tags='payments')
                elif number_changed and len(number_digits) < 13:
                    messages.error(request, tr(request, 'msg.card.full_number'), extra_tags='payments')
                elif len(cvv) != 3 or not cvv.isdigit():
                    messages.error(request, tr(request, 'msg.card.cvv'), extra_tags='payments')
                else:
                    card.exp_month = int(exp_month)
                    card.exp_year = int(exp_year)
                    card.holder_name = holder or sanitize_holder_name(user.get_full_name())
                    card.brand = brand
                    card.cvv = cvv
                    if number_changed:
                        card.pan = number_digits
                        card.last4 = number_digits[-4:]
                    card.save()
                    messages.success(request, tr(request, 'msg.card.updated'), extra_tags='payments')

        elif form_type == 'delete_card':
            card_id = request.POST.get('card_id')
            deleted, _ = PaymentCard.objects.filter(user=user, pk=card_id).delete()
            if deleted:
                messages.success(request, tr(request, 'msg.card.deleted'), extra_tags='payments')
                if not user.payment_cards.filter(is_default=True).exists():
                    first = user.payment_cards.first()
                    if first:
                        first.is_default = True
                        first.save(update_fields=['is_default'])
            else:
                messages.error(request, tr(request, 'msg.card.not_found'), extra_tags='payments')

        elif form_type == 'default_card':
            card = PaymentCard.objects.filter(user=user, pk=request.POST.get('card_id')).first()
            if card:
                card.is_default = True
                card.save()
                messages.success(request, tr(request, 'msg.card.default_updated'), extra_tags='payments')
            else:
                messages.error(request, tr(request, 'msg.card.not_found'), extra_tags='payments')

        else:
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()

            if not first_name or not email:
                messages.error(request, tr(request, 'msg.profile.required'), extra_tags='profile')
            elif not phone:
                messages.error(request, tr(request, 'msg.profile.phone_required'), extra_tags='profile')
            elif len(''.join(c for c in phone if c.isdigit())) > 15:
                messages.error(request, tr(request, 'msg.profile.phone_too_long'), extra_tags='profile')
            elif User.objects.filter(username=email).exclude(pk=user.pk).exists():
                messages.error(request, tr(request, 'msg.profile.email_taken'), extra_tags='profile')
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = email
                user.phone = phone
                if request.FILES.get('avatar'):
                    user.avatar = request.FILES['avatar']
                user.save()
                messages.success(request, tr(request, 'msg.profile.saved'), extra_tags='profile')
            anchor = 'profile'

        return redirect(reverse('profile') + '#' + anchor)

    return render(request, 'profile.html', {
        'needs_phone': not user.has_phone,
        'payment_cards': user.payment_cards.all(),
    })


@login_required
def password_view(request):
    success = None
    error = None

    if request.method == 'POST':
        current = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        new_password2 = request.POST.get('new_password2', '')

        if not request.user.check_password(current):
            error = tr(request, 'msg.password.wrong_current')
        elif not new_password:
            error = tr(request, 'msg.password.empty')
        elif new_password != new_password2:
            error = tr(request, 'msg.password.mismatch')
        else:
            request.user.set_password(new_password)
            request.user.save()
            mode = request.session.get('app_mode')
            login(request, request.user)
            if mode:
                set_app_mode(request, mode)
            success = tr(request, 'msg.password.updated')

    return render(request, 'password.html', {'success': success, 'error': error})


@login_required
def home_view(request):
    """Личная главная пассажира — быстрый доступ и обзор поездок."""
    user = request.user
    orders = Order.objects.filter(user=user)
    active_orders = orders.filter(status__in=ACTIVE_ORDER_STATUSES)
    active_order = active_orders.first()
    active_driver = get_driver_profile(active_order.driver_name) if active_order and active_order.driver_name else None
    recent_orders = orders[:4]
    done_count = orders.filter(status='done').count()

    total_km = sum(
        float(o.distance_km or 0) for o in orders.filter(status='done')
    )

    lang = resolve_language(request)
    return render(request, 'home.html', {
        'active_orders': active_orders,
        'active_order': active_order,
        'active_driver': active_driver,
        'passenger_rating': float(user.passenger_rating),
        'recent_orders': recent_orders,
        'done_count': done_count,
        'total_km': round(total_km, 1),
        'needs_phone': not user.has_phone,
        'tariff_catalog': translated_tariff_catalog(lang),
        'standard_tariffs': STANDARD_TARIFFS,
        'special_tariffs': SPECIAL_TARIFFS,
    })


@login_required
def order_page(request):
    user = request.user
    active = get_active_order(user)
    if active:
        return redirect('order_track', pk=active.pk)

    prefill_tariff = request.GET.get('tariff', 'economy')
    if prefill_tariff not in TARIFF_CATALOG:
        prefill_tariff = 'economy'
    prefill_to = request.GET.get('to', '').strip()[:255]
    prefill_from = request.GET.get('from', '').strip()[:255]

    lang = resolve_language(request)
    return render(request, 'order.html', {
        'needs_phone': not user.has_phone,
        'has_phone': user.has_phone,
        'user_phone': user.phone.strip() if user.phone else '',
        'prefill_tariff': prefill_tariff,
        'prefill_to': prefill_to,
        'prefill_from': prefill_from,
        'tariff_catalog': translated_tariff_catalog(lang),
        'standard_tariffs': STANDARD_TARIFFS,
        'special_tariffs': SPECIAL_TARIFFS,
        'payment_cards': user.payment_cards.all(),
        'default_card': user.payment_cards.filter(is_default=True).first(),
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    active_orders = orders.filter(status__in=ACTIVE_ORDER_STATUSES)
    return render(request, 'order_history.html', {
        'orders': orders,
        'active_orders': active_orders,
    })


@login_required
def order_track(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    driver = get_driver_profile(order.driver_name) if order.driver_name else None
    return render(request, 'order_track.html', {
        'order': order,
        'driver': driver,
        'driver_profiles_json': json.dumps(DRIVER_PROFILES),
    })


def dispatcher_user_required(view):
    return user_passes_test(
        lambda u: u.is_active and u.can_dispatch,
        login_url='dispatcher_login',
    )(view)


def dispatcher_mode_required(view):
    """Диспетчерская только после входа через /dispatcher/login/."""

    @login_required
    @dispatcher_user_required
    def wrapper(request, *args, **kwargs):
        if not is_dispatcher_mode(request):
            return redirect('dispatcher_login')
        return view(request, *args, **kwargs)

    return wrapper


@dispatcher_mode_required
def dispatcher_page(request):
    lang = resolve_language(request)
    orders = list(dispatch_orders_queryset())
    drivers = ['Klaus M.', 'Anna S.', 'Thomas B.', 'Maria K.', 'Stefan R.']
    context = {
        'orders': orders,
        'drivers': drivers,
        'counts': count_orders_by_status(orders),
        'dispatch_config': {
            'drivers': drivers,
            'orders': [serialize_dispatch_order(o, lang) for o in orders],
        },
    }
    return render(request, 'dispatcher.html', context)
