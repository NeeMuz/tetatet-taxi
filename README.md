# Tetatet Taxi

Веб-приложение для заказа такси: регистрация, оформление поездки, история заказов, диспетчерская панель и Django-админка.

## Возможности

- **Клиент:** регистрация, заказ такси, ориентировочная цена, live-обновление статуса
- **История:** все заказы пользователя в одном месте
- **Диспетчерская:** панель для сотрудников (`/dispatcher/`) — смена статусов в реальном времени
- **Админка:** `/admin/` — полное управление заказами, массовые действия, фильтры
- **API:** REST (`/api/taxi/orders/`) и GraphQL (`/graphql/`)
- **WebSocket:** `ws://host/ws/orders/` — уведомления о новых и изменённых заказах

## Быстрый старт (Windows)

```powershell
cd D:\Tetatet

# 1. Виртуальное окружение
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Зависимости
pip install -r requirements.txt

# 3. Настройки (скопируйте и при необходимости отредактируйте)
copy .env.example .env

# 4. База данных
python manage.py migrate

# 5. Суперпользователь (для админки и диспетчерской)
python manage.py createsuperuser

# 6. Статика (нужно при DEBUG=False)
python manage.py collectstatic --noinput

# 7. Запуск (HTTP + WebSocket)
daphne -b 127.0.0.1 -p 8000 tetatet.asgi:application
```

Откройте в браузере: **http://127.0.0.1:8000/**

### Альтернатива (только HTTP, без WebSocket)

```powershell
python manage.py runserver
```

## Роли пользователей

| Роль | Как получить | Доступ |
|------|--------------|--------|
| Клиент | Регистрация на сайте | Заказ, история, свой статус |
| Диспетчер | `is_staff=True` в админке | + `/dispatcher/`, все заказы |
| Админ | `is_superuser=True` | + `/admin/`, полный доступ |

После входа диспетчер автоматически попадает на `/dispatcher/`.

## Статусы заказа

`Новый` → `Принят` → `В пути` → `Завершён` (или `Отменён`)

Изменение статуса в админке или диспетчерской мгновенно отправляется клиенту через WebSocket.

## API

### REST

```
GET  /api/taxi/orders/          — список (свои заказы / все для staff)
POST /api/taxi/orders/          — создать заказ
GET  /api/taxi/orders/<id>/     — детали заказа
PATCH /api/taxi/orders/<id>/    — сменить статус (только staff)
```

Требуется авторизация (сессия). Для POST/PATCH передавайте CSRF-токен.

### GraphQL

- Endpoint: `/graphql/`
- GraphiQL включён
- Требуется авторизация

## Production (Railway)

`Procfile` уже настроен:

```
web: daphne -b 0.0.0.0 -p 8080 tetatet.asgi:application
```

Переменные окружения:

- `SECRET_KEY` — обязательно смените
- `DEBUG=False`
- `ALLOWED_HOSTS` — ваш домен
- `REDIS_URL` — для WebSocket между процессами
- PostgreSQL через `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

## Структура проекта

```
tetatet/       — настройки Django
accounts/      — регистрация, вход, страницы
taxi/          — заказы, API, WebSocket, админка
templates/     — HTML-шаблоны
static/        — CSS
```

## Стек

Django 6, DRF, Channels, Graphene, WhiteNoise, Daphne, SQLite (dev) / PostgreSQL (prod)
