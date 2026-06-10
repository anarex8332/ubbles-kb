// RUBBLES KB — Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Feather Icons — заменяет data-feather на SVG
    if (typeof feather !== 'undefined') {
        feather.replace({ width: 20, height: 20 });
    }

    // Auto-dismiss messages after 5 seconds
    document.querySelectorAll('.msg').forEach(function(msg) {
        setTimeout(function() {
            msg.style.opacity = '0';
            msg.style.transition = 'opacity 0.5s';
            setTimeout(function() { msg.remove(); }, 500);
        }, 5000);
    });

    // Highlight active nav link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(function(link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('nav-link--active');
        }
    });

    // Theme toggle
    initThemeToggle();
});

// ===== THEME TOGGLE (switch) =====
function initThemeToggle() {
    const toggle = document.getElementById('theme-toggle');
    if (!toggle) return;

    // Load saved theme
    const saved = localStorage.getItem('rubbles-theme') || 'light';
    if (saved === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        toggle.checked = true;
    }

    toggle.addEventListener('change', function() {
        if (this.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('rubbles-theme', 'dark');
        } else {
            document.documentElement.removeAttribute('data-theme');
            localStorage.setItem('rubbles-theme', 'light');
        }
    });
}
