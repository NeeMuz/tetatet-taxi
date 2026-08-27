document.addEventListener('DOMContentLoaded', () => {
    initAvatarPicker();
    initCardForm();
    initCardEdits();
    initDeleteCards();
    initHolderInputs();
    scrollToHash();
});

function scrollToHash() {
    const hash = window.location.hash;
    if (!hash) return;
    const el = document.querySelector(hash);
    if (!el) return;
    requestAnimationFrame(() => {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
}

function initAvatarPicker() {
    const tt = (k, fb) => (window.TETATET_I18N && window.TETATET_I18N[k]) || fb;
    const input = document.getElementById('avatarInput');
    const btn = document.getElementById('avatarFileBtn');
    const preview = document.getElementById('avatarPreview');
    const nameEl = document.getElementById('avatarFileName');
    if (!input || !btn) return;

    btn.addEventListener('click', () => input.click());

    input.addEventListener('change', () => {
        const file = input.files?.[0];
        if (!file) {
            if (nameEl) nameEl.textContent = tt('profile_avatar_hint', 'JPG, PNG — до 5 МБ');
            return;
        }
        if (nameEl) nameEl.textContent = file.name;
        if (preview && file.type.startsWith('image/')) {
            const url = URL.createObjectURL(file);
            preview.innerHTML = `<img src="${url}" alt="${tt('profile_avatar_preview', 'Превью')}">`;
        }
    });
}

function initDeleteCards() {
    const tt = (k, fb) => (window.TETATET_I18N && window.TETATET_I18N[k]) || fb;
    let armedBtn = null;
    let armedTimer = null;

    const disarm = (btn) => {
        if (!btn) return;
        btn.classList.remove('is-armed');
        btn.textContent = tt('profile_delete_card', 'Удалить');
    };

    document.querySelectorAll('.btn-delete-card').forEach((btn) => {
        btn.addEventListener('click', () => {
            const form = btn.closest('form');
            if (!form) return;

            if (armedBtn && armedBtn !== btn) {
                clearTimeout(armedTimer);
                disarm(armedBtn);
            }

            if (!btn.classList.contains('is-armed')) {
                armedBtn = btn;
                btn.classList.add('is-armed');
                btn.textContent = tt('profile_delete_confirm', 'Удалить точно?');
                clearTimeout(armedTimer);
                armedTimer = setTimeout(() => {
                    disarm(btn);
                    if (armedBtn === btn) armedBtn = null;
                }, 5000);
                return;
            }

            clearTimeout(armedTimer);
            armedBtn = null;
            form.submit();
        });
    });
}

function initCardForm() {
    const tt = (k, fb) => (window.TETATET_I18N && window.TETATET_I18N[k]) || fb;
    const form = document.getElementById('addCardForm');
    const numberInput = document.getElementById('cardNumber');
    const expiryInput = document.getElementById('cardExpiry');
    const cvvInput = document.getElementById('cardCvv');
    const holderInput = document.getElementById('cardHolder');
    const brandInput = document.getElementById('cardBrand');
    const brandBtn = document.getElementById('cardBrandBtn');
    const brandMenu = document.getElementById('cardBrandMenu');
    const userName = form?.dataset.userName || '';

    if (!numberInput || !form) return;

    setupBrandPicker(brandBtn, brandMenu, brandInput, document.getElementById('cardBrandIcon'));

    numberInput.addEventListener('input', () => {
        const digits = numberInput.value.replace(/\D/g, '').slice(0, 16);
        numberInput.value = formatCardNumber(digits);
        applyBrandFromDigits(digits, brandInput, brandBtn, document.getElementById('cardBrandIcon'));
        if (digits.length === 16) expiryInput?.focus();
    });

    expiryInput?.addEventListener('input', () => {
        const digits = expiryInput.value.replace(/\D/g, '').slice(0, 4);
        expiryInput.value = formatExpiry(digits);
        if (digits.length === 4) cvvInput?.focus();
    });

    cvvInput?.addEventListener('input', () => {
        cvvInput.value = cvvInput.value.replace(/\D/g, '').slice(0, 3);
        if (cvvInput.value.length === 3) holderInput?.focus();
    });

    holderInput?.addEventListener('input', () => {
        holderInput.value = sanitizeHolderName(holderInput.value);
    });

    cvvInput?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            fillHolderName(holderInput, userName);
        }
    });

    holderInput?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !holderInput.value.trim()) {
            e.preventDefault();
            fillHolderName(holderInput, userName);
        }
    });

    form.addEventListener('submit', (e) => {
        const number = numberInput.value.replace(/\s/g, '');
        applyBrandFromDigits(number, brandInput, brandBtn, document.getElementById('cardBrandIcon'));
        if (!brandInput.value) brandInput.value = 'other';

        const cvv = cvvInput?.value.trim() || '';
        const expiry = expiryInput?.value.replace(/\s/g, '') || '';

        if (number.length < 13) {
            e.preventDefault();
            alert(tt('payment_err_full_number', 'Введите полный номер карты'));
            numberInput.focus();
            return;
        }
        if (!/^\d{2}\/\d{2}$/.test(expiry)) {
            e.preventDefault();
            alert(tt('payment_err_expiry_format', 'Укажите срок действия в формате ММ/ГГ'));
            expiryInput?.focus();
            return;
        }
        if (cvv.length !== 3) {
            e.preventDefault();
            alert(tt('payment_err_cvv', 'Введите CVV (3 цифры)'));
            cvvInput?.focus();
        }
    });
}

function initCardEdits() {
    document.querySelectorAll('[data-edit-card]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const id = btn.dataset.editCard;
            const panel = document.getElementById('editCard-' + id);
            if (!panel) return;
            const isOpen = !panel.hidden;
            document.querySelectorAll('.payment-card-edit').forEach((p) => { p.hidden = true; });
            document.querySelectorAll('[data-edit-card]').forEach((b) => b.classList.remove('is-active'));
            if (!isOpen) {
                panel.hidden = false;
                btn.classList.add('is-active');
                panel.querySelector('input, select')?.focus();
            }
        });
    });

    document.querySelectorAll('.payment-card-edit-form').forEach((form) => {
        const expiryInput = form.querySelector('[data-edit-expiry]');
        const numberInput = form.querySelector('[data-edit-number]');
        const brandBtn = form.querySelector('[data-edit-brand-btn]');
        const brandMenu = form.querySelector('[data-edit-brand-menu]');
        const brandInput = form.querySelector('[data-edit-brand]');
        const brandIcon = form.querySelector('[data-edit-brand-icon]');

        setupBrandPicker(brandBtn, brandMenu, brandInput, brandIcon, true);

        expiryInput?.addEventListener('input', () => {
            const digits = expiryInput.value.replace(/\D/g, '').slice(0, 4);
            expiryInput.value = formatExpiry(digits);
        });

        form.querySelector('[data-edit-cvv]')?.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/\D/g, '').slice(0, 3);
        });

        numberInput?.addEventListener('input', () => {
            const digits = numberInput.value.replace(/\D/g, '').slice(0, 16);
            numberInput.value = formatCardNumber(digits);
            applyBrandFromDigits(digits, brandInput, brandBtn, brandIcon);
        });
    });
}

function initHolderInputs() {
    document.querySelectorAll('[name="holder_name"]').forEach((input) => {
        input.addEventListener('input', () => {
            input.value = sanitizeHolderName(input.value);
        });
        if (input.value) input.value = sanitizeHolderName(input.value);
    });
}

function sanitizeHolderName(value) {
    return (value || '')
        .replace(/[^a-zA-Zа-яА-ЯёЁ\s\-']/g, '')
        .toUpperCase();
}

function setupBrandPicker(btn, menu, input, iconEl, preselected) {
    if (!btn || !menu || !input) return;

    const setBrand = (brand, skipFocus) => {
        input.value = brand;
        btn.classList.add('is-selected');
        if (iconEl) {
            if (brand === 'visa') {
                iconEl.textContent = 'VISA';
                iconEl.className = 'card-brand-badge card-brand-badge--visa';
            } else if (brand === 'mastercard') {
                iconEl.textContent = 'MC';
                iconEl.className = 'card-brand-badge card-brand-badge--mc';
            } else {
                iconEl.textContent = '💳';
                iconEl.className = 'card-brand-badge card-brand-badge--empty';
            }
        }
        menu.hidden = true;
        btn.setAttribute('aria-expanded', 'false');
        if (!skipFocus) document.getElementById('cardNumber')?.focus();
    };

    if (preselected && input.value) {
        setBrand(input.value, true);
    }

    btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const open = menu.hidden;
        document.querySelectorAll('.card-brand-menu').forEach((m) => { m.hidden = true; });
        menu.hidden = !open;
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    menu.querySelectorAll('[data-brand]').forEach((item) => {
        item.addEventListener('click', () => setBrand(item.dataset.brand, !!preselected));
    });

    document.addEventListener('click', () => {
        menu.hidden = true;
        btn.setAttribute('aria-expanded', 'false');
    });
}

function detectBrandFromDigits(digits) {
    if (!digits) return '';
    if (digits[0] === '4') return 'visa';
    if (digits[0] === '5') return 'mastercard';
    return 'other';
}

function clearBrand(brandInput, brandBtn, iconEl) {
    if (brandInput) brandInput.value = '';
    brandBtn?.classList.remove('is-selected');
    if (iconEl) {
        iconEl.textContent = '💳';
        iconEl.className = 'card-brand-badge card-brand-badge--empty';
    }
}

function applyBrandFromDigits(digits, brandInput, brandBtn, iconEl) {
    if (!digits) {
        clearBrand(brandInput, brandBtn, iconEl);
        return;
    }
    const brand = detectBrandFromDigits(digits);
    brandInput.value = brand;
    brandBtn?.classList.add('is-selected');
    if (!iconEl) return;
    if (brand === 'visa') {
        iconEl.textContent = 'VISA';
        iconEl.className = 'card-brand-badge card-brand-badge--visa';
    } else if (brand === 'mastercard') {
        iconEl.textContent = 'MC';
        iconEl.className = 'card-brand-badge card-brand-badge--mc';
    } else {
        iconEl.textContent = '💳';
        iconEl.className = 'card-brand-badge card-brand-badge--empty';
    }
}

function formatCardNumber(digits) {
    return digits.replace(/(\d{4})(?=\d)/g, '$1 ').trim();
}

function formatExpiry(digits) {
    if (digits.length >= 3) return digits.slice(0, 2) + ' / ' + digits.slice(2);
    return digits;
}

function fillHolderName(input, name) {
    if (!input || !name) return;
    input.value = name.toUpperCase();
    input.focus();
}
