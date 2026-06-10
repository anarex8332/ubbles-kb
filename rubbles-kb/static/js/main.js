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

    // Emoji picker for textareas
    initEmojiPickers();
});

// ===== EMOJI PICKER =====
const EMOJIS = [
    '😀','😃','😄','😁','😅','😂','🤣','😊','😇','🙂',
    '🥰','😍','🤩','😘','😗','😚','😋','😛','😜','🤪',
    '😎','🤓','🧐','😳','🥺','😢','😤','😡','🤬','😈',
    '👍','👎','👊','✊','🤛','🤜','👏','🙌','🤝','💪',
    '❤️','🧡','💛','💚','💙','💜','🖤','🤍','💔','💖',
    '🔥','⭐','✨','💡','📝','✅','❌','⚠️','🚀','🎯',
    '📁','📂','📄','📅','📊','📈','🔍','🔒','🔓','💻',
    '🏢','👥','📋','⚙️','🧩','🔐','🎯','📜','🏷️','📦',
    '💰','☁️','🔄','⚡','🛠️','🧪','🎨','📎','🔗','✏️',
];

function initEmojiPickers() {
    document.querySelectorAll('.emoji-enabled').forEach(function(textarea) {
        // Find form-group parent
        const formGroup = textarea.closest('.form-group') || textarea.parentNode;

        // Create toolbar below the textarea
        const toolbar = document.createElement('div');
        toolbar.className = 'emoji-toolbar';
        toolbar.style.cssText = 'display:flex;gap:4px;margin-top:4px;align-items:center;';

        // Emoji button
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.innerHTML = '😊';
        btn.title = 'Вставить emoji';
        btn.style.cssText = 'background:var(--bg-card);border:1px solid var(--border);border-radius:3px;cursor:pointer;font-size:16px;padding:2px 8px;line-height:1.5;';
        btn.onmouseover = function() { this.style.borderColor = 'var(--primary)'; };
        btn.onmouseout = function() { this.style.borderColor = 'var(--border)'; };

        // Hint text
        const hint = document.createElement('span');
        hint.textContent = 'Нажмите для вставки emoji';
        hint.style.cssText = 'font-size:11px;color:var(--text-muted);';

        toolbar.appendChild(btn);
        toolbar.appendChild(hint);
        formGroup.appendChild(toolbar);

        // Create picker (absolutely positioned relative to the textarea)
        const picker = document.createElement('div');
        picker.className = 'emoji-picker';
        picker.style.cssText = 'display:none;position:absolute;z-index:100;background:white;border:1px solid var(--border);border-radius:6px;box-shadow:var(--shadow-lg);padding:8px;width:320px;max-height:200px;overflow-y:auto;grid-template-columns:repeat(10,1fr);gap:2px;';

        // Position picker relative to textarea
        textarea.style.position = 'relative';

        // Populate emojis
        EMOJIS.forEach(function(emoji) {
            const span = document.createElement('span');
            span.textContent = emoji;
            span.style.cssText = 'cursor:pointer;padding:4px;text-align:center;border-radius:3px;font-size:20px;display:inline-block;';
            span.onmouseover = function() { this.style.background = 'var(--border-light)'; };
            span.onmouseout = function() { this.style.background = 'transparent'; };
            span.onclick = function() {
                insertEmoji(textarea, emoji);
                picker.style.display = 'none';
            };
            picker.appendChild(span);
        });

        // Position and append picker
        picker.style.position = 'absolute';
        picker.style.bottom = (toolbar.offsetHeight + 8) + 'px';
        picker.style.left = '0';

        // Insert picker after textarea but before toolbar
        formGroup.insertBefore(picker, toolbar);

        // Toggle picker
        btn.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            const isVisible = picker.style.display === 'grid';
            // Close all pickers
            document.querySelectorAll('.emoji-picker').forEach(function(p) { p.style.display = 'none'; });
            picker.style.display = isVisible ? 'none' : 'grid';
            // Reposition
            picker.style.bottom = (toolbar.offsetHeight + 36) + 'px';
        };

        // Close on outside click
        document.addEventListener('click', function(e) {
            if (!toolbar.contains(e.target) && !picker.contains(e.target)) {
                picker.style.display = 'none';
            }
        });
    });
}

function insertEmoji(textarea, emoji) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;
    textarea.value = text.substring(0, start) + emoji + text.substring(end);
    textarea.selectionStart = textarea.selectionEnd = start + emoji.length;
    textarea.focus();
    const event = new Event('input', { bubbles: true });
    textarea.dispatchEvent(event);
}
