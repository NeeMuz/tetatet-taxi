"""Снятие актуальных скриншотов приложения Tetatet для документации."""
import os
import sys
from pathlib import Path

import django

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tetatet.settings')
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from taxi.models import Order  # noqa: E402

from playwright.sync_api import sync_playwright  # noqa: E402

BASE = 'http://127.0.0.1:8000'
OUT = Path(__file__).resolve().parent / 'screenshots'
OUT.mkdir(parents=True, exist_ok=True)

PASS_EMAIL = 'pdf.passenger@tetatet.local'
PASS_PASSWORD = 'PdfPassenger2026!'
DISP_EMAIL = 'pdf.dispatcher@tetatet.local'
DISP_PASSWORD = 'PdfDispatcher2026!'


def ensure_users():
    User = get_user_model()
    passenger, _ = User.objects.get_or_create(
        username='pdf_passenger',
        defaults={
            'email': PASS_EMAIL,
            'first_name': 'Anna',
            'last_name': 'Müller',
            'phone': '+49 170 1234567',
        },
    )
    passenger.email = PASS_EMAIL
    passenger.first_name = 'Anna'
    passenger.last_name = 'Müller'
    passenger.phone = '+49 170 1234567'
    passenger.is_dispatcher = False
    passenger.set_password(PASS_PASSWORD)
    passenger.is_active = True
    passenger.save()

    dispatcher, _ = User.objects.get_or_create(
        username='pdf_dispatcher',
        defaults={
            'email': DISP_EMAIL,
            'first_name': 'Operator',
            'last_name': 'Desk',
        },
    )
    dispatcher.email = DISP_EMAIL
    dispatcher.is_dispatcher = True
    dispatcher.is_staff = True
    dispatcher.set_password(DISP_PASSWORD)
    dispatcher.is_active = True
    dispatcher.save()

    Order.objects.filter(user=passenger).delete()
    Order.objects.create(
        user=passenger,
        name='Anna Müller',
        phone='+49 170 1234567',
        from_address='Brandenburger Tor, Berlin',
        to_address='Alexanderplatz, Berlin',
        tariff='comfort',
        distance_km=3.2,
        estimated_price=12.50,
        status='on_way',
        driver_name='Klaus M.',
    )
    Order.objects.create(
        user=passenger,
        name='Anna Müller',
        phone='+49 170 1234567',
        from_address='Hauptbahnhof, Berlin',
        to_address='Flughafen Berlin BER',
        tariff='economy',
        distance_km=28.5,
        estimated_price=42.30,
        status='done',
        driver_name='Anna S.',
    )

    return passenger


def shot(page, name: str, url: str | None = None, wait_ms: int = 1200):
    if url:
        page.goto(url, wait_until='networkidle', timeout=45000)
    page.wait_for_timeout(wait_ms)
    path = OUT / f'{name}.png'
    page.screenshot(path=str(path), full_page=False)
    print(f'  OK {path.name}')
    return path


def login_passenger(page):
    page.goto(f'{BASE}/login/', wait_until='networkidle')
    page.fill('input[name="email"]', PASS_EMAIL)
    page.fill('input[name="password"]', PASS_PASSWORD)
    page.click('button[type="submit"]')
    page.wait_for_url('**/order/**', timeout=20000)


def login_dispatcher(page):
    page.goto(f'{BASE}/dispatcher/login/', wait_until='networkidle')
    page.fill('input[name="email"]', DISP_EMAIL)
    page.fill('input[name="password"]', DISP_PASSWORD)
    page.click('button[type="submit"]')
    page.wait_for_url('**/dispatcher/**', timeout=20000)


def main():
    ensure_users()
    tracking_id = Order.objects.filter(user__email=PASS_EMAIL, status='on_way').values_list('id', flat=True).first()
    print('Capturing screenshots...')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1440, 'height': 900},
            locale='ru-RU',
        )
        page = context.new_page()

        shot(page, '01-landing', f'{BASE}/')

        login_passenger(page)
        shot(page, '02-order', wait_ms=2500)

        page.fill('#from', 'Brandenburger Tor, Berlin')
        page.fill('#to', 'Alexanderplatz, Berlin')
        page.wait_for_timeout(3500)
        shot(page, '03-order-route', wait_ms=800)

        shot(page, '04-profile', f'{BASE}/profile/')
        shot(page, '05-history', f'{BASE}/orders/')

        if tracking_id:
            shot(page, '06-tracking', f'{BASE}/orders/{tracking_id}/', wait_ms=2500)

        page.goto(f'{BASE}/logout/', wait_until='networkidle')
        page.wait_for_timeout(600)
        shot(page, '07-dispatcher-login', f'{BASE}/dispatcher/login/')

        login_dispatcher(page)
        page.wait_for_timeout(2500)
        shot(page, '08-dispatcher-panel', wait_ms=1000)

        browser.close()

    print(f'Done: {len(list(OUT.glob("*.png")))} files in {OUT}')


if __name__ == '__main__':
    main()
