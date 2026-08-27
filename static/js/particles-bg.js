(function () {
    const canvas = document.getElementById('particlesBg');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let particles = [];
    let w = 0;
    let h = 0;
    let mouse = { x: -9999, y: -9999, active: false };

    const REPEL_RADIUS = 110;
    const FALL_SPEED = 0.35;

    function resize() {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    }

    function spawnParticle(resetY) {
        return {
            x: Math.random() * w,
            y: resetY ? -Math.random() * h * 0.2 : Math.random() * h,
            vx: (Math.random() - 0.5) * 0.25,
            vy: FALL_SPEED + Math.random() * 0.55,
            r: Math.random() * 1.6 + 0.35,
            red: Math.random() > 0.38,
            alpha: Math.random() * 0.45 + 0.25,
            wobble: Math.random() * Math.PI * 2,
        };
    }

    function init() {
        const count = Math.min(110, Math.floor((w * h) / 12000));
        particles = Array.from({ length: count }, () => spawnParticle(false));
    }

    function applyMouseRepulsion(p) {
        if (!mouse.active) return;
        const dx = p.x - mouse.x;
        const dy = p.y - mouse.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist > REPEL_RADIUS || dist < 1) return;

        const force = (REPEL_RADIUS - dist) / REPEL_RADIUS;
        p.vx += (dx / dist) * force * 0.35;
        p.vy += (dy / dist) * force * 0.35;
    }

    function draw() {
        ctx.clearRect(0, 0, w, h);

        particles.forEach((p) => {
            applyMouseRepulsion(p);

            p.wobble += 0.012;
            p.vx += Math.sin(p.wobble) * 0.004;
            p.vx *= 0.99;
            p.vy = Math.max(p.vy, FALL_SPEED * 0.6);

            p.x += p.vx;
            p.y += p.vy;

            if (p.x < -10) p.x = w + 10;
            if (p.x > w + 10) p.x = -10;

            if (p.y > h + 12) {
                p.x = Math.random() * w;
                p.y = -8 - Math.random() * 40;
                p.vy = FALL_SPEED + Math.random() * 0.55;
                p.vx = (Math.random() - 0.5) * 0.25;
            }

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.red
                ? `rgba(255, 0, 51, ${p.alpha})`
                : `rgba(255, 255, 255, ${p.alpha * 0.4})`;
            ctx.fill();
        });

        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const a = particles[i];
                const b = particles[j];
                const dx = a.x - b.x;
                const dy = a.y - b.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 85) {
                    ctx.strokeStyle = `rgba(255, 0, 51, ${0.05 * (1 - dist / 85)})`;
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(a.x, a.y);
                    ctx.lineTo(b.x, b.y);
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(draw);
    }

    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
        mouse.active = true;
    });

    window.addEventListener('mouseleave', () => {
        mouse.active = false;
    });

    window.addEventListener('resize', () => {
        resize();
        init();
    });

    resize();
    init();
    draw();
})();
