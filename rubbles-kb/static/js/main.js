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

    // Emoji picker
    initEmojiPicker();
});

// ===== EMOJI PICKER =====
const EMOJIS = [
    '😀', '😃', '😄', '😁', '😅', '😂', '🤣', '😊', '😇', '🙂',
    '🥰', '😍', '🤩', '😘', '😗', '😚', '😋', '😛', '😜', '🤪',
    '😎', '🤓', '🧐', '😳', '🥺', '😢', '😤', '😡', '🤬', '😈',
    '👍', '👎', '👊', '✊', '🤛', '🤜', '👏', '🙌', '🤝', '💪',
    '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '💔', '💖',
    '🔥', '⭐', '✨', '💡', '📝', '✅', '❌', '⚠️', '🚀', '🎯',
    '📁', '📂', '📄', '📅', '📊', '📈', '🔍', '🔒', '🔓', '💻',
    '🏢', '👥', '📋', '⚙️', '🧩', '🔐', '🎯', '📜', '🏷️', '📦',
    '💰', '☁️', '🔄', '⚡', '🛠️', '🧪', '🎨', '📎', '🔗', '✏️',
];

function initEmojiPicker() {
    const textareas = document.querySelectorAll('.emoji-enabled');
    textareas.forEach(function(textarea) {
        // Create container
        const wrapper = document.createElement('div');
        wrapper.style.position = 'relative';

        // Create emoji button
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.innerHTML = '😊';
        btn.title = 'Вставить emoji';
        btn.style.cssText = 'position:absolute;bottom:8px;right:8px;background:var(--bg-card);border:1px solid var(--border);border-radius:3px;cursor:pointer;font-size:18px;padding:4px 6px;line-height:1;z-index:2;';
        btn.onmouseover = function() { this.style.borderColor = 'var(--primary)'; };
        btn.onmouseout = function() { this.style.borderColor = 'var(--border)'; };

        // Create picker
        const picker = document.createElement('div');
        picker.className = 'emoji-picker';
        picker.style.cssText = 'display:none;position:absolute;bottom:42px;right:0;background:white;border:1px solid var(--border);border-radius:6px;box-shadow:var(--shadow-lg);padding:8px;width:320px;max-height:200px;overflow-y:auto;z-index:10;grid-template-columns:repeat(10,1fr);gap:2px;';

        // Populate emojis
        EMOJIS.forEach(function(emoji) {
            const span = document.createElement('span');
            span.textContent = emoji;
            span.style.cssText = 'cursor:pointer;padding:4px;text-align:center;border-radius:3px;font-size:20px;';
            span.onmouseover = function() { this.style.background = 'var(--border-light)'; };
            span.onmouseout = function() { this.style.background = 'transparent'; };
            span.onclick = function() {
                insertEmoji(textarea, emoji);
                picker.style.display = 'none';
            };
            picker.appendChild(span);
        });

        // Toggle picker
        btn.onclick = function(e) {
            e.preventDefault();
            picker.style.display = picker.style.display === 'none' || picker.style.display === '' ? 'grid' : 'none';
        };

        // Close picker on outside click
        document.addEventListener('click', function(e) {
            if (!wrapper.contains(e.target)) {
                picker.style.display = 'none';
            }
        });

        // Insert wrapper
        textarea.parentNode.insertBefore(wrapper, textarea);
        wrapper.appendChild(textarea);
        wrapper.appendChild(btn);
        wrapper.appendChild(picker);
    });
}

function insertEmoji(textarea, emoji) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;
    textarea.value = text.substring(0, start) + emoji + text.substring(end);
    textarea.selectionStart = textarea.selectionEnd = start + emoji.length;
    textarea.focus();

    // Trigger input event for any listeners
    const event = new Event('input', { bubbles: true });
    textarea.dispatchEvent(event);
}