// ===== JAVASCRIPT ДЛЯ СТРАНИЦЫ РЕДАКТИРОВАНИЯ ПРОФИЛЯ =====

(function() {
    'use strict';

    // Состояние аватара
    let avatarState = {
        originalSrc: null,
        hasOriginal: false,
        isModified: false,
        fileToUpload: null,
        markedForDelete: false
    };

    document.addEventListener('DOMContentLoaded', function() {
        initAvatarClick();
        initCustomUploadButton();
        initRemoveAvatarButton();
        initFormSubmit();
        initResetButton();
        
        // Сохраняем оригинальное состояние
        const avatarImg = document.getElementById('avatar-image');
        if (avatarImg) {
            avatarState.originalSrc = avatarImg.src;
            avatarState.hasOriginal = true;
        }
    });

    // Инициализация клика по аватару
    function initAvatarClick() {
        const clickableAvatar = document.getElementById('clickable-avatar');
        const avatarUpload = document.getElementById('avatar-upload');
        
        if (clickableAvatar && avatarUpload) {
            clickableAvatar.addEventListener('click', function() {
                avatarUpload.click();
            });
        }
    }

    // Инициализация кастомной кнопки загрузки
    function initCustomUploadButton() {
        const uploadBtn = document.getElementById('custom-upload-btn');
        const avatarUpload = document.getElementById('avatar-upload');
        
        if (uploadBtn && avatarUpload) {
            uploadBtn.addEventListener('click', function() {
                avatarUpload.click();
            });
        }

        if (avatarUpload) {
            avatarUpload.addEventListener('change', handleAvatarSelect);
        }
    }

    // Обработка выбора файла
    function handleAvatarSelect(e) {
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

        // Сохраняем файл для отправки
        avatarState.fileToUpload = file;
        avatarState.isModified = true;
        avatarState.markedForDelete = false;

        // Синхронизируем с полем Django формы
        syncFileToDjangoField(file);

        // Показываем превью
        const reader = new FileReader();
        reader.onload = function(e) {
            updateAvatarPreview(e.target.result);
            showModifiedIndicator();
            hideError();
        };
        reader.readAsDataURL(file);
    }

    // Синхронизация файла с полем Django формы
    function syncFileToDjangoField(file) {
        const djangoField = document.getElementById('id_avatar');
        if (djangoField) {
            // Создаем новый FileList с нашим файлом
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            djangoField.files = dataTransfer.files;
            
            // Триггерим событие change для Django (на всякий случай)
            const event = new Event('change', { bubbles: true });
            djangoField.dispatchEvent(event);
        }
    }

    // Обновление превью аватара
    function updateAvatarPreview(imageSrc) {
        const container = document.getElementById('clickable-avatar');
        const existingImg = document.getElementById('avatar-image');
        const existingPlaceholder = document.getElementById('avatar-placeholder');
        const overlay = container.querySelector('.avatar-overlay');
        
        // Удаляем существующее содержимое
        container.innerHTML = '';
        
        // Создаем новый img
        const img = document.createElement('img');
        img.id = 'avatar-image';
        img.src = imageSrc;
        img.alt = 'Аватар';
        img.className = 'current-avatar';
        
        container.appendChild(img);
        container.appendChild(overlay);
        
        // Обновляем состояние кнопки удаления
        document.getElementById('remove-avatar-btn').disabled = false;
    }

    // Показать placeholder
    function showPlaceholder() {
        const container = document.getElementById('clickable-avatar');
        const overlay = container.querySelector('.avatar-overlay');
        
        container.innerHTML = '';
        
        const placeholder = document.createElement('div');
        placeholder.id = 'avatar-placeholder';
        placeholder.className = 'avatar-placeholder';
        placeholder.innerHTML = '<div class="avatar-lg bg-secondary rounded-circle d-flex align-items-center justify-content-center mb-3"><i class="fas fa-user fa-4x text-white"></i></div>';
        
        container.appendChild(placeholder);
        container.appendChild(overlay);
        
        // Обновляем состояние
        avatarState.fileToUpload = null;
        avatarState.isModified = true;
        avatarState.markedForDelete = true;
        
        // Очищаем поле загрузки и поле Django
        document.getElementById('avatar-upload').value = '';
        const djangoField = document.getElementById('id_avatar');
        if (djangoField) {
            djangoField.value = '';
        }
        
        // Блокируем кнопку удаления
        document.getElementById('remove-avatar-btn').disabled = true;
    }

    // Инициализация кнопки удаления
    function initRemoveAvatarButton() {
        const removeBtn = document.getElementById('remove-avatar-btn');
        if (!removeBtn) return;

        removeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showPlaceholder();
            showModifiedIndicator();
            hideError();
        });
    }

    // Показать индикатор изменений
    function showModifiedIndicator() {
        const indicator = document.getElementById('avatar-modified-indicator');
        if (indicator) {
            indicator.style.display = 'inline-block';
        }
    }

    // Скрыть индикатор изменений
    function hideModifiedIndicator() {
        const indicator = document.getElementById('avatar-modified-indicator');
        if (indicator) {
            indicator.style.display = 'none';
        }
    }

    // Показать ошибку
    function showError(message) {
        const errorContainer = document.getElementById('avatar-errors');
        if (errorContainer) {
            errorContainer.textContent = message;
        }
    }

    // Скрыть ошибку
    function hideError() {
        const errorContainer = document.getElementById('avatar-errors');
        if (errorContainer) {
            errorContainer.textContent = '';
        }
    }

    // Инициализация отправки формы
    function initFormSubmit() {
        const form = document.getElementById('profile-form');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            // Если нужно удалить аватар (показываем placeholder, но оригинал был)
            if (avatarState.markedForDelete && avatarState.hasOriginal) {
                // Добавляем скрытое поле для удаления
                const clearField = document.createElement('input');
                clearField.type = 'hidden';
                clearField.name = 'clear_avatar';
                clearField.value = 'true';
                form.appendChild(clearField);
            }
            
            // Файл уже должен быть в djangoField через syncFileToDjangoField
            // Ничего дополнительно делать не нужно
        });
    }

    // Инициализация кнопки сброса
    function initResetButton() {
        const resetBtn = document.getElementById('reset-btn');
        if (!resetBtn) return;

        resetBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (confirm('Отменить все изменения?')) {
                resetToOriginal();
            }
        });
    }

    // Сброс к оригинальному состоянию
    function resetToOriginal() {
        const container = document.getElementById('clickable-avatar');
        const overlay = container.querySelector('.avatar-overlay');
        
        if (avatarState.hasOriginal) {
            // Был оригинальный аватар
            container.innerHTML = '';
            
            const img = document.createElement('img');
            img.id = 'avatar-image';
            img.src = avatarState.originalSrc;
            img.alt = 'Аватар';
            img.className = 'current-avatar';
            
            container.appendChild(img);
            container.appendChild(overlay);
            
            document.getElementById('remove-avatar-btn').disabled = false;
            
            // Очищаем поле Django
            const djangoField = document.getElementById('id_avatar');
            if (djangoField) {
                djangoField.value = '';
            }
        } else {
            // Оригинала не было - показываем placeholder
            container.innerHTML = '';
            
            const placeholder = document.createElement('div');
            placeholder.id = 'avatar-placeholder';
            placeholder.className = 'avatar-placeholder';
            placeholder.innerHTML = '<i class="fas fa-user"></i>';
            
            container.appendChild(placeholder);
            container.appendChild(overlay);
            
            document.getElementById('remove-avatar-btn').disabled = true;
        }
        
        // Сбрасываем состояние
        avatarState.isModified = false;
        avatarState.fileToUpload = null;
        avatarState.markedForDelete = false;
        
        // Скрываем индикатор
        hideModifiedIndicator();
        
        // Очищаем поле загрузки
        document.getElementById('avatar-upload').value = '';
        
        // Скрываем ошибки
        hideError();
    }

})();