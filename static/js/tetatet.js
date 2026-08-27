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

function tt(key, fallback = '') {
    return (window.TETATET_I18N && window.TETATET_I18N[key]) || fallback;
}

function togglePassword(inputId, btn) {
    const input = document.getElementById(inputId);
    if (!input) return;
    if (input.type === 'password') {
        input.type = 'text';
        btn.textContent = tt('common_hide', 'Скрыть');
    } else {
        input.type = 'password';
        btn.textContent = tt('common_show', 'Показать');
    }
}

const STATUS_LABELS = {
    new: tt('status_new', 'Ожидает водителя'),
    accepted: tt('status_accepted', 'Такси едет к вам'),
    arrived: tt('status_arrived', 'Такси на месте'),
    on_way: tt('status_on_way', 'В пути к пункту назначения'),
    done: tt('status_done', 'Поездка завершена'),
    cancelled: tt('status_cancelled', 'Отменён'),
};

const TARIFF_LABELS = {
    economy: tt('tariff_economy_display', 'Economy'),
    comfort: tt('tariff_comfort_display', 'Comfort'),
    business: tt('tariff_business_display', 'Business'),
    minivan: tt('tariff_minivan_display', 'Minivan'),
    cargo: tt('tariff_cargo_display', 'Cargo'),
    pets: tt('tariff_pets_display', 'PetRide'),
    kids: tt('tariff_kids_display', 'Family'),
};

const TARIFF_MULTIPLIERS = {
    economy: 1.0,
    comfort: 1.4,
    business: 1.85,
    minivan: 2.25,
    cargo: 2.1,
    pets: 1.25,
    kids: 1.15,
};

const ALL_TARIFFS = ['economy', 'comfort', 'business', 'minivan', 'cargo', 'pets', 'kids'];

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

async function passengerOrderAction(orderId, status) {
    const res = await fetch(`/api/taxi/orders/${orderId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'same-origin',
        body: JSON.stringify({ status }),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        const msg = err.status?.[0] || err.detail || tt('common_error', 'Ошибка');
        alert(msg);
        return null;
    }
    return res.json();
}

async function submitTripRating(orderId, rating) {
    const res = await fetch(`/api/taxi/orders/${orderId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'same-origin',
        body: JSON.stringify({ trip_rating: rating }),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        const msg = err.trip_rating?.[0] || err.detail || tt('common_error', 'Ошибка');
        alert(msg);
        return null;
    }
    return res.json();
}

function renderStarDisplay(container, rating) {
    if (!container) return;
    const value = Math.max(0, Math.min(5, parseFloat(rating) || 0));
    container.innerHTML = '';
    for (let i = 1; i <= 5; i++) {
        const star = document.createElement('span');
        star.className = 'star' + (i <= Math.round(value) ? ' on' : '');
        star.textContent = '★';
        container.appendChild(star);
    }
}

function initStarDisplays(root) {
    (root || document).querySelectorAll('.star-display[data-rating]').forEach((el) => {
        renderStarDisplay(el, el.dataset.rating);
    });
}

function buildStarRatingWidget(onSelect) {
    const wrap = document.createElement('div');
    wrap.className = 'star-rate';
    let selected = 0;

    for (let i = 1; i <= 5; i++) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'star-rate-btn';
        btn.dataset.value = String(i);
        btn.textContent = '★';
        btn.addEventListener('mouseenter', () => highlight(i));
        btn.addEventListener('mouseleave', () => highlight(selected));
        btn.addEventListener('click', () => {
            selected = i;
            highlight(selected);
            onSelect?.(selected);
        });
        wrap.appendChild(btn);
    }

    function highlight(upTo) {
        wrap.querySelectorAll('.star-rate-btn').forEach((b) => {
            b.classList.toggle('on', Number(b.dataset.value) <= upTo);
        });
    }

    return wrap;
}

function mountSlideCancel(container, onConfirm) {
    if (!container) return;
    container.innerHTML = `
        <div class="slide-cancel">
            <div class="slide-cancel-fill"></div>
            <span class="slide-cancel-label">${tt('common_cancel_slide', 'Сдвиньте для отмены')}</span>
            <button type="button" class="slide-cancel-thumb" aria-label="${tt('common_cancel_slide', 'Сдвиньте для отмены')}">»</button>
        </div>`;

    const track = container.querySelector('.slide-cancel');
    const thumb = container.querySelector('.slide-cancel-thumb');
    const fill = container.querySelector('.slide-cancel-fill');
    let dragging = false;
    let thumbX = 0;
    let maxX = 0;
    let triggered = false;

    function measure() {
        maxX = Math.max(0, track.clientWidth - thumb.offsetWidth - 8);
    }

    function setPos(x) {
        thumbX = Math.max(0, Math.min(maxX, x));
        thumb.style.transform = `translateX(${thumbX}px)`;
        fill.style.width = `${thumbX + thumb.offsetWidth * 0.5}px`;
    }

    function reset() {
        if (triggered) return;
        thumbX = 0;
        thumb.style.transform = '';
        fill.style.width = '0';
        track.classList.remove('slide-cancel--done');
    }

    function finish() {
        if (triggered) return;
        triggered = true;
        track.classList.add('slide-cancel--done');
        fill.style.width = '100%';
        thumb.style.transform = `translateX(${maxX}px)`;
        onConfirm?.();
    }

    function pointerX(e) {
        const rect = track.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        return clientX - rect.left - thumb.offsetWidth / 2 - 4;
    }

    thumb.addEventListener('mousedown', (e) => {
        e.preventDefault();
        measure();
        dragging = true;
    });
    thumb.addEventListener('touchstart', (e) => {
        measure();
        dragging = true;
    }, { passive: true });

    window.addEventListener('mousemove', (e) => {
        if (!dragging || triggered) return;
        setPos(pointerX(e));
        if (thumbX >= maxX * 0.85) finish();
    });
    window.addEventListener('touchmove', (e) => {
        if (!dragging || triggered) return;
        setPos(pointerX(e));
        if (thumbX >= maxX * 0.85) finish();
    }, { passive: true });

    const endDrag = () => {
        if (!dragging) return;
        dragging = false;
        if (!triggered && thumbX < maxX * 0.85) reset();
    };
    window.addEventListener('mouseup', endDrag);
    window.addEventListener('touchend', endDrag);

    window.addEventListener('resize', measure);
    setTimeout(measure, 50);
}

document.addEventListener('DOMContentLoaded', () => initStarDisplays());

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
        const msg = err.status?.[0] || err.driver_name?.[0] || err.detail || tt('common_error', 'Ошибка');
        alert(msg);
        return null;
    }
    return res.json();
}

function initHeaderNavGlider() {
    const root = document.querySelector('[data-header-nav]');
    const track = root?.querySelector('.header-nav-track');
    if (!track) return;

    const glider = track.querySelector('.header-nav-glider');
    const items = [...track.querySelectorAll('.header-nav-item')];
    if (!glider || !items.length) return;

    const NAV_MS = 460;
    const LAST_TAB_KEY = 'tetatet_nav_tab';
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const active = () => track.querySelector('.header-nav-item.is-active');

    const placeGlider = (item, animate, resting = false) => {
        if (!item) {
            glider.style.removeProperty('opacity');
            glider.classList.remove('is-resting');
            return;
        }
        glider.style.removeProperty('opacity');
        glider.classList.toggle('is-resting', resting);
        glider.style.setProperty('--nav-x', `${item.offsetLeft}px`);
        glider.style.setProperty('--nav-w', `${item.offsetWidth}px`);
        glider.classList.toggle('no-transition', !animate);
    };

    const edgeSquash = (index) => {
        glider.classList.remove('is-squash-left', 'is-squash-right');
        void glider.offsetWidth;
        if (index <= 0) glider.classList.add('is-squash-left');
        else if (index >= items.length - 1) glider.classList.add('is-squash-right');
        window.setTimeout(() => {
            glider.classList.remove('is-squash-left', 'is-squash-right');
        }, 480);
    };

    const activeItem = active();
    const lastIdx = parseInt(sessionStorage.getItem(LAST_TAB_KEY), 10);
    const restingItem = activeItem
        || ((!Number.isNaN(lastIdx) && items[lastIdx]) ? items[lastIdx] : null);

    if (restingItem) {
        placeGlider(restingItem, false, !activeItem);
        if (activeItem) {
            sessionStorage.setItem(LAST_TAB_KEY, String(items.indexOf(activeItem)));
        }
        requestAnimationFrame(() => glider.classList.remove('no-transition'));
    }

    items.forEach((item, index) => {
        item.addEventListener('click', (e) => {
            if (item.classList.contains('is-active')) return;
            if (track.dataset.navBusy === '1') {
                e.preventDefault();
                return;
            }

            const href = item.getAttribute('href');
            if (!href) return;

            sessionStorage.setItem(LAST_TAB_KEY, String(index));

            if (prefersReducedMotion) return;

            e.preventDefault();
            track.dataset.navBusy = '1';
            track.classList.add('is-animating');

            items.forEach((el) => el.classList.remove('is-active'));
            item.classList.add('is-active');
            placeGlider(item, true, false);

            let done = false;
            const go = () => {
                if (done) return;
                done = true;
                window.location.href = href;
            };

            const isEdge = index === 0 || index === items.length - 1;
            const totalDelay = NAV_MS + (isEdge ? 220 : 0) + 40;

            window.setTimeout(() => {
                if (isEdge) edgeSquash(index);
            }, NAV_MS - 20);

            window.setTimeout(go, totalDelay);
        });
    });

    window.addEventListener('resize', () => {
        if (track.dataset.navBusy === '1') return;
        const current = active() || ((!Number.isNaN(parseInt(sessionStorage.getItem(LAST_TAB_KEY), 10)) && items[parseInt(sessionStorage.getItem(LAST_TAB_KEY), 10)]) || null);
        if (current) placeGlider(current, false);
    });
}

document.addEventListener('DOMContentLoaded', initHeaderNavGlider);
