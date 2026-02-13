// ===== JAVASCRIPT ДЛЯ СТРАНИЦЫ РЕДАКТИРОВАНИЯ ПРОФИЛЯ =====

(function() {
    'use strict';

    // Инициализация при загрузке DOM
    document.addEventListener('DOMContentLoaded', function() {
        initAvatarPreview();
        initRemoveAvatarButton();
        initResetButton();
        initPhoneFormatter();
        initFormLeaveWarning();
    });

    // Инициализация предпросмотра аватара
    function initAvatarPreview() {
        const avatarInput = document.getElementById('id_avatar');
        const avatarPreview = document.getElementById('avatar-preview');
        const fileInfo = document.getElementById('file-info');
        const avatarLabel = document.querySelector('.avatar-upload-label');

        if (!avatarInput) return;

        avatarInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (!file) return;

            // Проверка размера файла (2MB)
            if (file.size > 2 * 1024 * 1024) {
                showError('Файл слишком большой. Максимальный размер - 2MB.');
                this.value = '';
                return;
            }

            // Проверка типа файла
            const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
            if (!validTypes.includes(file.type)) {
                showError('Пожалуйста, выберите изображение в формате JPG, PNG, GIF или WebP.');
                this.value = '';
                return;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                updateAvatarPreview(e.target.result, file.name);
            };
            reader.readAsDataURL(file);
        });
    }

    // Обновление превью аватара
    function updateAvatarPreview(imageSrc, fileName) {
        const avatarPreview = document.getElementById('avatar-preview');
        const fileInfo = document.getElementById('file-info');
        const avatarContainer = document.querySelector('.avatar-upload-container');
        
        if (avatarPreview) {
            avatarPreview.src = imageSrc;
            avatarPreview.classList.add('current-avatar');
        } else {
            // Создаем новый preview если его нет
            const label = document.querySelector('.avatar-upload-label');
            const newPreview = document.createElement('img');
            newPreview.id = 'avatar-preview';
            newPreview.src = imageSrc;
            newPreview.alt = 'Новый аватар';
            newPreview.classList.add('current-avatar');
            
            // Удаляем плейсхолдер если есть
            const placeholder = document.querySelector('.avatar-placeholder');
            if (placeholder) {
                placeholder.remove();
            }
            
            label.insertBefore(newPreview, label.querySelector('.avatar-upload-overlay'));
        }

        // Обновляем информацию о файле
        if (fileInfo) {
            fileInfo.innerHTML = `<span class="badge bg-info">
                <i class="fas fa-cloud-upload-alt me-1"></i>Новое фото: ${fileName || 'выбрано'}
            </span>`;
        }
    }

    // Инициализация кнопки удаления аватара
    function initRemoveAvatarButton() {
        const removeBtn = document.getElementById('remove-avatar-btn');
        if (!removeBtn) return;

        removeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            showConfirmationDialog(
                'Удаление фото профиля',
                'Вы уверены, что хотите удалить фото профиля?',
                function() {
                    const form = document.getElementById('profile-form');
                    const removeField = document.createElement('input');
                    removeField.type = 'hidden';
                    removeField.name = 'remove_avatar';
                    removeField.value = 'true';
                    form.appendChild(removeField);
                    form.submit();
                }
            );
        });
    }

    // Инициализация кнопки сброса
    function initResetButton() {
        const resetBtn = document.getElementById('reset-btn');
        if (!resetBtn) return;

        resetBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            showConfirmationDialog(
                'Сброс изменений',
                'Все несохраненные изменения будут потеряны. Продолжить?',
                function() {
                    const form = document.getElementById('profile-form');
                    form.reset();
                    restoreOriginalAvatar();
                    showNotification('Форма сброшена', 'info');
                }
            );
        });
    }

    // Восстановление оригинального аватара
    function restoreOriginalAvatar() {
        const avatarPreview = document.getElementById('avatar-preview');
        const fileInfo = document.getElementById('file-info');
        
        {% if user.has_avatar %}
        if (avatarPreview) {
            avatarPreview.src = '{{ user.avatar.url }}';
        }
        {% endif %}
        
        if (fileInfo) {
            {% if user.has_avatar %}
            fileInfo.innerHTML = '<span class="badge bg-success"><i class="fas fa-check me-1"></i>Текущее фото</span>';
            {% else %}
            fileInfo.innerHTML = '<span class="text-white-50"><i class="fas fa-info-circle me-1"></i>Фото не загружено</span>';
            {% endif %}
        }
    }

    // Инициализация форматирования телефона
    function initPhoneFormatter() {
        const phoneInput = document.getElementById('id_phone');
        if (!phoneInput) return;

        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 0) {
                // Добавляем +7 в начало
                if (value.length <= 11) {
                    value = '+7' + value.slice(1);
                }
                
                // Форматирование
                if (value.length <= 2) {
                    value = value;
                } else if (value.length <= 5) {
                    value = value.slice(0, 2) + ' (' + value.slice(2, 5);
                } else if (value.length <= 8) {
                    value = value.slice(0, 2) + ' (' + value.slice(2, 5) + ') ' + value.slice(5, 8);
                } else if (value.length <= 10) {
                    value = value.slice(0, 2) + ' (' + value.slice(2, 5) + ') ' + value.slice(5, 8) + '-' + value.slice(8, 10);
                } else {
                    value = value.slice(0, 2) + ' (' + value.slice(2, 5) + ') ' + value.slice(5, 8) + '-' + value.slice(8, 10) + '-' + value.slice(10, 12);
                }
                
                e.target.value = value;
            }
        });

        // Форматируем при потере фокуса
        phoneInput.addEventListener('blur', function(e) {
            if (e.target.value) {
                e.target.value = window.formatPhoneNumber(e.target.value);
            }
        });
    }

    // Предупреждение о несохраненных изменениях
    function initFormLeaveWarning() {
        const form = document.getElementById('profile-form');
        if (!form) return;

        let formChanged = false;

        form.addEventListener('change', function() {
            formChanged = true;
        });

        form.addEventListener('input', function() {
            formChanged = true;
        });

        window.addEventListener('beforeunload', function(e) {
            if (formChanged) {
                e.preventDefault();
                e.returnValue = '';
                return '';
            }
        });

        form.addEventListener('submit', function() {
            formChanged = false;
        });
    }

    // Показ ошибки
    function showError(message) {
        alert(message); // Можно заменить на красивое уведомление
        console.error(message);
    }

})();