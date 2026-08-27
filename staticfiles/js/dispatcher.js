const DISPATCH_API = '/api/taxi/dispatch/orders/';

const COL_MAP = {
    new: 'colNew',
    accepted: 'colAccepted',
    on_way: 'colOnWay',
    done: 'colDone',
    cancelled: 'colCancelled',
};

function formatDispatchPrice(value) {
    const num = parseFloat(String(value).replace(',', '.'));
    if (Number.isNaN(num)) return '—';
    return '$' + num.toFixed(2);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text == null ? '' : String(text);
    return div.innerHTML;
}

async function runDispatchAction(btn) {
    if (!btn || btn.disabled || btn.dataset.busy === '1') return;

    const id = btn.dataset.id;
    const action = btn.dataset.action;
    if (!id || !action) return;

    let payload = {};

    if (action === 'accept') {
        const sel = document.querySelector(`.driver-select[data-for="${id}"]`);
        if (!sel?.value) {
            alert('Выберите водителя');
            return;
        }
        payload = { status: 'accepted', driver_name: sel.value };
    } else if (action === 'on_way') {
        payload = { status: 'on_way' };
    } else if (action === 'done') {
        payload = { status: 'done' };
    } else if (action === 'cancel') {
        if (!confirm('Отменить заказ #' + id + '?')) return;
        payload = { status: 'cancelled' };
    } else {
        return;
    }

    btn.dataset.busy = '1';
    btn.disabled = true;
    const oldText = btn.textContent;
    btn.textContent = '...';

    try {
        if (typeof dispatchOrder !== 'function') {
            alert('Скрипт не загружен. Нажмите Ctrl+F5.');
            return;
        }
        const result = await dispatchOrder(id, payload);
        if (result && window.dispatchBoard) {
            const idx = window.dispatchBoard.orders.findIndex(o => Number(o.id) === Number(id));
            if (idx >= 0) {
                window.dispatchBoard.orders[idx] = { ...window.dispatchBoard.orders[idx], ...result };
            }
            window.dispatchBoard.render();
        } else if (result) {
            location.reload();
        }
    } catch (err) {
        console.error('Dispatch action error', err);
        alert('Ошибка при выполнении действия');
    } finally {
        btn.disabled = false;
        btn.textContent = oldText;
        btn.dataset.busy = '0';
    }
}

window._runDispatchAction = runDispatchAction;

class DispatchBoard {
    constructor(config) {
        this.orders = config.orders || [];
        this.drivers = config.drivers || [];
        this.searchQuery = '';
        this._bindUi();

        const hasSsrCards = !!document.querySelector('#dispatchBoard .dispatch-card');
        if (!hasSsrCards) {
            this.render();
        }

        this.reload();
        this._connectSocket();
        this._pollTimer = setInterval(() => this.reload(), 30000);
    }

    _bindUi() {
        const board = document.getElementById('dispatchBoard');
        if (board) {
            board.addEventListener('click', (e) => {
                const btn = e.target.closest('button[data-action]');
                if (!btn || btn.disabled) return;
                e.preventDefault();
                runDispatchAction(btn);
            });
        }

        document.getElementById('dispatchSearch')?.addEventListener('input', (e) => {
            this.searchQuery = e.target.value.trim().toLowerCase();
            this.render();
        });

        document.getElementById('dispatchRefresh')?.addEventListener('click', () => this.reload());
    }

    _showError(msg) {
        const el = document.getElementById('dispatchError');
        if (!el) return;
        el.textContent = msg || '';
        el.style.display = msg ? 'block' : 'none';
    }

    async reload() {
        try {
            const res = await fetch(DISPATCH_API, { credentials: 'same-origin' });
            if (!res.ok) {
                this._showError(`Не удалось обновить (ошибка ${res.status}). Показаны данные с сервера.`);
                return;
            }
            const data = await res.json();
            if (!Array.isArray(data)) return;
            this.orders = data;
            this._showError('');
            const total = document.getElementById('totalOrders');
            if (total) total.textContent = this.orders.length;
            this.render();
        } catch (e) {
            console.warn('Dispatch reload error', e);
            this._showError('Ошибка сети. Показаны данные с сервера.');
        }
    }

    _connectSocket() {
        if (typeof connectOrderSocket !== 'function') return;
        connectOrderSocket((data) => {
            const idx = this.orders.findIndex(o => Number(o.id) === Number(data.id));
            const normalized = {
                id: data.id,
                status: data.status,
                name: data.name,
                phone: data.phone,
                from_address: data.from_address,
                to_address: data.to_address,
                tariff: data.tariff,
                tariff_display: data.tariff_display,
                driver_name: data.driver_name || '',
                estimated_price: data.estimated_price,
                created_at: data.created_at,
            };
            if (idx >= 0) {
                this.orders[idx] = { ...this.orders[idx], ...normalized };
            } else {
                this.orders.unshift(normalized);
            }
            const total = document.getElementById('totalOrders');
            if (total) total.textContent = this.orders.length;
            this.render();
        });
    }

    _filteredOrders() {
        if (!this.searchQuery) return this.orders;
        return this.orders.filter(o => {
            const hay = [
                o.id, o.name, o.phone, o.from_address, o.to_address,
                o.driver_name, o.tariff_display,
            ].join(' ').toLowerCase();
            return hay.includes(this.searchQuery);
        });
    }

    _ordersForStatus(status) {
        return this._filteredOrders().filter(o => o.status === status);
    }

    render() {
        Object.entries(COL_MAP).forEach(([status, colId]) => {
            const col = document.getElementById(colId);
            if (!col) return;
            const orders = this._ordersForStatus(status);
            col.innerHTML = orders.length
                ? orders.map(o => this._cardHtml(o)).join('')
                : '<p class="dispatch-empty">Нет заказов</p>';
            const countEl = document.querySelector(`[data-count="${status}"]`);
            if (countEl) countEl.textContent = orders.length;
        });

        const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
        set('statNew', this._ordersForStatus('new').length);
        set('statAccepted', this._ordersForStatus('accepted').length);
        set('statOnWay', this._ordersForStatus('on_way').length);
        set('statDone', this._ordersForStatus('done').length);
    }

    _cardHtml(order) {
        const price = formatDispatchPrice(order.estimated_price);
        const labels = window.TARIFF_LABELS || { economy: 'Economy', comfort: 'Comfort', business: 'Business' };
        const tariff = escapeHtml(order.tariff_display || labels[order.tariff] || order.tariff);
        const route = `
            <div class="dispatch-card-route">
                <div class="r-from">${escapeHtml(order.from_address)}</div>
                <div class="r-to">${escapeHtml(order.to_address)}</div>
            </div>`;

        if (order.status === 'new') {
            const driverOpts = this.drivers.map(d =>
                `<option value="${escapeHtml(d)}">${escapeHtml(d)}</option>`
            ).join('');
            return `
            <div class="dispatch-card is-new" data-order-id="${order.id}">
                <div class="dispatch-card-top"><strong>#${order.id}</strong><span>${escapeHtml(order.created_at || '')}</span></div>
                ${route}
                <div class="dispatch-card-meta">
                    <span>${escapeHtml(order.name)} · ${tariff}</span>
                    <a href="tel:${escapeHtml(order.phone)}" class="dispatch-phone">${escapeHtml(order.phone)}</a>
                </div>
                <div class="dispatch-card-price-row">${price}</div>
                <div class="dispatch-actions">
                    <select class="driver-select" data-for="${order.id}">
                        <option value="">Выберите водителя</option>
                        ${driverOpts}
                    </select>
                    <button type="button" class="btn-dispatch btn-dispatch-accept" data-action="accept" data-id="${order.id}">Назначить водителя</button>
                    <button type="button" class="btn-dispatch btn-dispatch-cancel" data-action="cancel" data-id="${order.id}">Отклонить</button>
                </div>
            </div>`;
        }

        if (order.status === 'accepted') {
            return `
            <div class="dispatch-card" data-order-id="${order.id}">
                <div class="dispatch-card-top"><strong>#${order.id}</strong><span>${tariff}</span></div>
                ${route}
                <div class="dispatch-card-meta">
                    <span>🚕 ${escapeHtml(order.driver_name || '—')}</span>
                    <a href="tel:${escapeHtml(order.phone)}" class="dispatch-phone">${escapeHtml(order.phone)}</a>
                </div>
                <div class="dispatch-card-price-row">${price}</div>
                <div class="dispatch-actions">
                    <button type="button" class="btn-dispatch btn-dispatch-go" data-action="on_way" data-id="${order.id}">Водитель выехал</button>
                    <button type="button" class="btn-dispatch btn-dispatch-cancel" data-action="cancel" data-id="${order.id}">Отменить</button>
                </div>
            </div>`;
        }

        if (order.status === 'on_way') {
            return `
            <div class="dispatch-card" data-order-id="${order.id}">
                <div class="dispatch-card-top"><strong>#${order.id}</strong><span>${escapeHtml(order.phone)}</span></div>
                ${route}
                <div class="dispatch-card-meta">
                    <span>🚕 ${escapeHtml(order.driver_name || '—')}</span>
                    <span class="dispatch-card-price">${price}</span>
                </div>
                <div class="dispatch-actions">
                    <button type="button" class="btn-dispatch btn-dispatch-done" data-action="done" data-id="${order.id}">Завершить поездку</button>
                </div>
            </div>`;
        }

        if (order.status === 'done' || order.status === 'cancelled') {
            return `
            <div class="dispatch-card dispatch-card-done" data-order-id="${order.id}">
                <div class="dispatch-card-top"><strong>#${order.id}</strong><span>${escapeHtml(order.created_at || '')}</span></div>
                <div class="dispatch-card-route muted">
                    ${escapeHtml((order.from_address || '').slice(0, 40))} → ${escapeHtml((order.to_address || '').slice(0, 40))}
                </div>
                <div class="dispatch-card-meta">
                    <span>${escapeHtml(order.driver_name || order.name || '—')}</span>
                    <span class="dispatch-card-price">${price}</span>
                </div>
            </div>`;
        }

        return '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const el = document.getElementById('dispatchData');
    let config = { drivers: [], orders: [] };
    if (el) {
        try {
            config = JSON.parse(el.textContent);
        } catch (e) {
            console.error('Dispatch JSON parse error', e);
        }
    }
    try {
        window.dispatchBoard = new DispatchBoard(config);
    } catch (e) {
        console.error('DispatchBoard init error', e);
    }
});
