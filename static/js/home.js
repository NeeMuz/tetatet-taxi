document.addEventListener('DOMContentLoaded', () => {
    const tt = (k, fb) => (window.TETATET_I18N && window.TETATET_I18N[k]) || fb;
    const hour = new Date().getHours();
    const greetEl = document.getElementById('homeGreeting');

    if (greetEl) {
        let key = 'greeting_day';
        if (hour < 6) key = 'greeting_night';
        else if (hour < 12) key = 'greeting_morning';
        else if (hour >= 18) key = 'greeting_evening';
        greetEl.textContent = tt(key, 'Добрый день');
    }

    document.querySelectorAll('.home-stat-card strong[data-count]').forEach((el) => {
        const target = parseFloat(el.dataset.count || '0');
        const decimals = parseInt(el.dataset.decimals || '0', 10);
        const duration = 900;
        const start = performance.now();

        const tick = (now) => {
            const p = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - p, 3);
            const val = target * eased;
            el.textContent = decimals ? val.toFixed(decimals) : Math.round(val);
            if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
    });

    document.querySelectorAll('.home-dest-chip').forEach((chip) => {
        chip.addEventListener('click', () => {
            const to = encodeURIComponent(chip.dataset.to || '');
            window.location.href = `/order/?to=${to}`;
        });
    });

    if (typeof initStarDisplays === 'function') {
        initStarDisplays();
    }

    const orderBar = document.getElementById('homeOrderBar');
    if (orderBar && !orderBar.classList.contains('home-order-bar--active')) {
        setInterval(() => {
            orderBar.classList.toggle('home-order-bar--pulse');
        }, 2800);
    }

    if (typeof createSimpleMap === 'function') {
        createSimpleMap('homeMap', true);
    }
});
