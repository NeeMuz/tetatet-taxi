document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-lang-dropdown]').forEach(initLangDropdown);
});

function initLangDropdown(root) {
    const form = root.querySelector('.lang-dropdown-form');
    const trigger = root.querySelector('.lang-dropdown-trigger');
    const menu = root.querySelector('.lang-dropdown-menu');
    const items = [...root.querySelectorAll('.lang-dropdown-item')];
    if (!form || !trigger || !menu) return;

    const placeholder = document.createComment('lang-menu-anchor');
    form.insertBefore(placeholder, menu);

    const closeAll = (except = null) => {
        document.querySelectorAll('[data-lang-dropdown].is-open').forEach((el) => {
            if (el === except) return;
            el.__closeLangMenu?.();
        });
    };

    const restoreMenu = () => {
        if (menu.parentNode !== form) {
            form.insertBefore(menu, placeholder);
        }
    };

    const positionMenu = () => {
        const rect = trigger.getBoundingClientRect();
        const width = Math.max(rect.width, 176);
        const left = Math.min(
            Math.max(8, rect.right - width),
            window.innerWidth - width - 8,
        );

        menu.style.position = 'fixed';
        menu.style.zIndex = '100000';
        menu.style.top = `${rect.bottom + 8}px`;
        menu.style.left = `${left}px`;
        menu.style.right = 'auto';
        menu.style.bottom = 'auto';
        menu.style.width = `${width}px`;
        menu.style.display = 'block';
    };

    const close = () => {
        menu.hidden = true;
        menu.style.cssText = '';
        menu.classList.remove('is-floating');
        restoreMenu();
        trigger.setAttribute('aria-expanded', 'false');
        root.classList.remove('is-open');
    };

    root.__closeLangMenu = close;

    const open = () => {
        closeAll(root);
        document.body.appendChild(menu);
        menu.hidden = false;
        menu.classList.add('is-floating');
        trigger.setAttribute('aria-expanded', 'true');
        root.classList.add('is-open');
        positionMenu();
    };

    trigger.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (root.classList.contains('is-open')) close();
        else open();
    });

    items.forEach((btn) => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();

            if (btn.classList.contains('is-active')) {
                close();
                return;
            }

            const csrf = form.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
            const next = form.querySelector('[name=next]')?.value || window.location.pathname;
            const language = btn.value;

            close();

            const body = new URLSearchParams();
            body.set('language', language);
            body.set('csrfmiddlewaretoken', csrf);
            body.set('next', next);

            try {
                await fetch(form.action, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': csrf,
                    },
                    body,
                    credentials: 'same-origin',
                });
            } catch (err) {
                console.error('Language switch failed', err);
            }

            window.location.assign(next);
        });
    });

    document.addEventListener('click', (e) => {
        if (!root.classList.contains('is-open')) return;
        if (root.contains(e.target) || menu.contains(e.target)) return;
        close();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && root.classList.contains('is-open')) close();
    });

    window.addEventListener('resize', () => {
        if (root.classList.contains('is-open')) positionMenu();
    });

    window.addEventListener('scroll', () => {
        if (root.classList.contains('is-open')) positionMenu();
    }, true);
}
