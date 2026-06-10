// RUBBLES KB — Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Автозакрытие сообщений через 5 секунд
    document.querySelectorAll('.message').forEach(function(msg) {
        setTimeout(function() {
            msg.style.opacity = '0';
            msg.style.transition = 'opacity 0.5s';
            setTimeout(function() { msg.remove(); }, 500);
        }, 5000);
    });

    // Подсветка активного раздела в сайдбаре
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(function(link) {
        if (link.getAttribute('href') === currentPath) {
            link.style.background = 'rgba(255,255,255,0.15)';
            link.style.color = 'var(--text-sidebar-active)';
        }
    });
});