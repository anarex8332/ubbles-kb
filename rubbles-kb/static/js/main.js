// RUBBLES KB — Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
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
});