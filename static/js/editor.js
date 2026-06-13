// RUBBLES KB — Article Editor
(function() {
    'use strict';

    let previewMode = false;
    let autoSaveTimer = null;
    let lastSaved = null;

    document.addEventListener('DOMContentLoaded', function() {
        window.editorEl = document.getElementById('editor-content');
        if (!window.editorEl) return;

        initToolbar();
        initAutoSave();
        initTags();
        initCustomSelect();
        initPreview();
        initTitleCounter();
        initDragDrop();
        restoreDraft();
    });

    // ===== TOOLBAR =====
    function initToolbar() {
        document.querySelectorAll('.editor-toolbar__btn').forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                var cmd = this.dataset.cmd;
                var val = this.dataset.value || null;
                if (cmd === 'createLink') {
                    var url = prompt('Введите URL:', 'https://');
                    if (url) document.execCommand(cmd, false, url);
                    return;
                }
                if (cmd === 'insertMermaid') {
                    insertMermaid();
                    return;
                }
                if (cmd === 'insertImage') {
                    document.getElementById('image-input').click();
                    return;
                }
                if (cmd === 'insertHr') {
                    document.execCommand('insertHorizontalRule');
                    return;
                }
                if (cmd === 'formatBlock') {
                    document.execCommand(cmd, false, val);
                    return;
                }
                document.execCommand(cmd, false, val);
                window.editorEl.focus();
            });
        });

        // Image upload handler
        var imgInput = document.getElementById('image-input');
        if (imgInput) {
            imgInput.addEventListener('change', function(e) {
                var file = e.target.files[0];
                if (file && file.type.startsWith('image/')) {
                    var reader = new FileReader();
                    reader.onload = function(ev) {
                        document.execCommand('insertImage', false, ev.target.result);
                        window.editorEl.focus();
                    };
                    reader.readAsDataURL(file);
                }
                this.value = '';
            });
        }
    }

    function insertMermaid() {
        var template = '<div class="mermaid">\ngraph TD\n    A[Начало] --> B[Шаг 1]\n    B --> C[Шаг 2]\n    C --> D[Конец]\n</div>\n<p><br></p>';
        document.execCommand('insertHTML', false, template);
    }

    // ===== TAGS =====
    function initTags() {
        var input = document.getElementById('tags-input');
        var container = document.getElementById('tags-container');
        var hidden = document.getElementById('tags-hidden');
        if (!input || !container || !hidden) return;

        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();
                addTag(this.value.trim());
            }
        });
        input.addEventListener('blur', function() {
            if (this.value.trim()) addTag(this.value.trim());
        });

        window.removeTag = function(el) {
            el.parentNode.removeChild(el);
            updateTagsHidden();
        };

        function addTag(text) {
            if (!text) return;
            var chips = container.querySelectorAll('.tag-chip');
            if (chips.length >= 10) return;
            for (var i = 0; i < chips.length; i++) {
                if (chips[i].dataset.tag === text.toLowerCase()) { input.value = ''; return; }
            }
            var chip = document.createElement('span');
            chip.className = 'tag-chip';
            chip.dataset.tag = text.toLowerCase();
            chip.innerHTML = text + '<button type="button" class="tag-chip__remove" onclick="removeTag(this.parentNode)">&times;</button>';
            container.insertBefore(chip, input);
            input.value = '';
            updateTagsHidden();
        }

        function updateTagsHidden() {
            var tags = [];
            container.querySelectorAll('.tag-chip').forEach(function(c) { tags.push(c.dataset.tag); });
            hidden.value = tags.join(',');
        }
    }

    // ===== CUSTOM SELECT (Section dropdown) =====
    function initCustomSelect() {
        var toggle = document.getElementById('section-toggle');
        var dropdown = document.getElementById('section-dropdown');
        var hidden = document.getElementById('section-hidden');
        if (!toggle || !dropdown || !hidden) return;

        toggle.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdown.classList.toggle('custom-select__dropdown--open');
        });

        dropdown.querySelectorAll('.custom-select__option').forEach(function(opt) {
            opt.addEventListener('click', function() {
                var val = this.dataset.value;
                var label = this.dataset.label;
                var icon = this.dataset.icon;
                hidden.value = val;
                toggle.innerHTML = '<span class="custom-select__toggle-icon">' + icon + '</span><span>' + label + '</span><i class="fas fa-chevron-down custom-select__toggle-arrow"></i>';
                dropdown.classList.remove('custom-select__dropdown--open');
            });
        });

        document.addEventListener('click', function() {
            dropdown.classList.remove('custom-select__dropdown--open');
        });

        var searchInput = dropdown.querySelector('.custom-select__search');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                var q = this.value.toLowerCase();
                dropdown.querySelectorAll('.custom-select__option').forEach(function(opt) {
                    opt.style.display = opt.dataset.label.toLowerCase().includes(q) ? '' : 'none';
                });
            });
        }
    }

    // ===== PREVIEW MODE =====
    function initPreview() {
        var btn = document.getElementById('preview-toggle');
        if (!btn) return;

        btn.addEventListener('click', function() {
            previewMode = !previewMode;
            if (previewMode) {
                window.editorEl.contentEditable = 'false';
                window.editorEl.classList.add('editor-content--preview');
                btn.innerHTML = '<i class="fas fa-edit"></i> Редактировать';
            } else {
                window.editorEl.contentEditable = 'true';
                window.editorEl.classList.remove('editor-content--preview');
                btn.innerHTML = '<i class="fas fa-eye"></i> Предпросмотр';
            }
        });
    }

    // ===== TITLE COUNTER =====
    function initTitleCounter() {
        var input = document.getElementById('title-input');
        var counter = document.getElementById('title-counter');
        if (!input || !counter) return;
        input.addEventListener('input', function() {
            counter.textContent = this.value.length + '/200';
            if (this.value.length > 190) counter.style.color = '#E53935';
            else counter.style.color = '#707579';
        });
    }

    // ===== DRAG & DROP INTO EDITOR =====
    function initDragDrop() {
        window.editorEl.addEventListener('dragover', function(e) {
            e.preventDefault();
            window.editorEl.classList.add('editor-content--dragover');
        });
        window.editorEl.addEventListener('dragleave', function(e) {
            window.editorEl.classList.remove('editor-content--dragover');
        });
        window.editorEl.addEventListener('drop', function(e) {
            e.preventDefault();
            window.editorEl.classList.remove('editor-content--dragover');
            var file = e.dataTransfer.files[0];
            if (file && file.type.startsWith('image/')) {
                var reader = new FileReader();
                reader.onload = function(ev) {
                    document.execCommand('insertImage', false, ev.target.result);
                };
                reader.readAsDataURL(file);
            }
        });

        window.editorEl.addEventListener('paste', function(e) {
            var items = e.clipboardData.items;
            for (var i = 0; i < items.length; i++) {
                if (items[i].type.startsWith('image/')) {
                    e.preventDefault();
                    var file = items[i].getAsFile();
                    var reader = new FileReader();
                    reader.onload = function(ev) {
                        document.execCommand('insertImage', false, ev.target.result);
                    };
                    reader.readAsDataURL(file);
                    return;
                }
            }
        });
    }

    // ===== AUTOSAVE =====
    function initAutoSave() {
        var indicator = document.getElementById('autosave-indicator');
        if (!indicator) return;

        window.editorEl.addEventListener('input', function() {
            indicator.textContent = 'Сохранение...';
            if (autoSaveTimer) clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(function() {
                saveDraft();
                indicator.textContent = 'Автосохранение: только что';
            }, 30000);
        });

        var form = document.getElementById('article-form');
        if (form) {
            form.addEventListener('submit', function() {
                syncEditorToTextarea();
                clearDraft();
            });
        }
    }

    function saveDraft() {
        var data = {
            title: document.getElementById('title-input') ? document.getElementById('title-input').value : '',
            content: window.editorEl.innerHTML,
            section: document.getElementById('section-hidden') ? document.getElementById('section-hidden').value : '',
            tags: document.getElementById('tags-hidden') ? document.getElementById('tags-hidden').value : ''
        };
        try {
            localStorage.setItem('rubbles-editor-draft', JSON.stringify(data));
        } catch(e) {}
    }

    function restoreDraft() {
        try {
            var raw = localStorage.getItem('rubbles-editor-draft');
            if (!raw) return;
            var data = JSON.parse(raw);
            if (data.title && document.getElementById('title-input') && !document.getElementById('title-input').value) {
                document.getElementById('title-input').value = data.title;
                var counter = document.getElementById('title-counter');
                if (counter) counter.textContent = data.title.length + '/200';
            }
            if (data.content && window.editorEl && !window.editorEl.innerHTML.trim()) {
                window.editorEl.innerHTML = data.content;
            }
        } catch(e) {}
    }

    function clearDraft() {
        try { localStorage.removeItem('rubbles-editor-draft'); } catch(e) {}
    }

    function syncEditorToTextarea() {
        var textarea = document.getElementById('content-hidden');
        if (textarea) textarea.value = window.editorEl.innerHTML;
    }

    // ===== ГЛОБАЛЬНЫЕ ФУНКЦИИ ДЛЯ КНОПОК ФОРМЫ =====
    window.syncEditorContent = function() {
        var hidden = document.getElementById('content-hidden');
        if (hidden && window.editorEl) hidden.value = window.editorEl.innerHTML;
    };

    window.setStatus = function(mode) {
        var status = document.getElementById('status-hidden');
        if (status) status.value = mode;
    };

    // ===== PUBLISH / DRAFT MODE =====
    window.setPublishMode = function(mode) {
        window.syncEditorContent();
        window.setStatus(mode);
        var btn = document.getElementById('real-submit-btn');
        if (btn) btn.click();
    };

})();
