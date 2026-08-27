function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function getCsrfToken() {
    return getCookie('csrftoken')
        || document.querySelector('[name=csrfmiddlewaretoken]')?.value
        || '';
}

function togglePassword(inputId, btn) {
    const input = document.getElementById(inputId);
    if (!input) return;
    if (input.type === 'password') {
        input.type = 'text';
        btn.textContent = 'Скрыть';
    } else {
        input.type = 'password';
        btn.textContent = 'Показать';
    }
}

const STATUS_LABELS = {
    new: 'Ожидает водителя',
    accepted: 'Водитель назначен',
    on_way: 'Водитель в пути',
    done: 'Поездка завершена',
    cancelled: 'Отменён',
};

const TARIFF_LABELS = {
    economy: 'Economy',
    comfort: 'Comfort',
    business: 'Business',
};

const TARIFF_MULTIPLIERS = { economy: 1.0, comfort: 1.4, business: 1.85 };

const BASE_FARE = 3.5;
const PER_KM = 1.25;

function calcPrice(distanceKm, tariff) {
    const mult = TARIFF_MULTIPLIERS[tariff] || 1;
    return Math.round((BASE_FARE + PER_KM * distanceKm) * mult * 100) / 100;
}

function formatPrice(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
    }).format(value);
}

function connectOrderSocket(onMessage) {
    const scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const socket = new WebSocket(`${scheme}://${window.location.host}/ws/orders/`);
    socket.onmessage = (event) => {
        try { onMessage(JSON.parse(event.data)); }
        catch (e) { console.warn('WS parse error', e); }
    };
    return socket;
}

async function dispatchOrder(orderId, payload) {
    const res = await fetch(`/api/taxi/orders/${orderId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'same-origin',
        body: JSON.stringify(payload),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        const msg = err.status?.[0] || err.driver_name?.[0] || err.detail || 'Ошибка';
        alert(msg);
        return null;
    }
    return res.json();
}
