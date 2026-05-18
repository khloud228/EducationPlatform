// ===== JAVASCRIPT ДЛЯ СТРАНИЦ АУТЕНТИФИКАЦИИ =====

(function() {
    'use strict';

    // Инициализация при загрузке DOM
    document.addEventListener('DOMContentLoaded', function() {
        initPasswordStrength();
        initPasswordMatch();
        initAutoHideAlerts();
        initEmailActions();
    });

    // Инициализация индикатора сложности пароля
    function initPasswordStrength() {
        const password1 = document.getElementById('id_password1');
        if (!password1) return;

        const strengthBar = document.getElementById('passwordStrength');
        
        // Элементы требований
        const reqLength = document.getElementById('req-length');
        const reqDigit = document.getElementById('req-digit');
        const reqUpper = document.getElementById('req-upper');
        const reqLower = document.getElementById('req-lower');
        const reqSpecial = document.getElementById('req-special');

        password1.addEventListener('input', function() {
            checkPasswordStrength(this.value);
        });

        function checkPasswordStrength(password) {
            const hasLength = password.length >= 8;
            const hasDigit = /\d/.test(password);
            const hasUpper = /[A-Z]/.test(password);
            const hasLower = /[a-z]/.test(password);
            const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);
            
            // Обновляем требования
            updateRequirement(reqLength, hasLength);
            updateRequirement(reqDigit, hasDigit);
            updateRequirement(reqUpper, hasUpper);
            updateRequirement(reqLower, hasLower);
            updateRequirement(reqSpecial, hasSpecial);
            
            // Считаем количество выполненных требований
            const score = [hasLength, hasDigit, hasUpper, hasLower, hasSpecial].filter(Boolean).length;
            
            // Обновляем индикатор
            if (strengthBar) {
                strengthBar.className = 'password-strength-bar';
                if (score <= 2) {
                    strengthBar.classList.add('strength-weak');
                } else if (score <= 4) {
                    strengthBar.classList.add('strength-medium');
                } else {
                    strengthBar.classList.add('strength-strong');
                }
            }
        }

        function updateRequirement(element, isValid) {
            if (!element) return;
            
            const icon = element.querySelector('i');
            if (isValid) {
                element.classList.add('valid');
                if (icon) icon.className = 'fas fa-check-circle';
            } else {
                element.classList.remove('valid');
                if (icon) icon.className = 'fas fa-circle';
            }
        }
    }

    // Инициализация проверки совпадения паролей
    function initPasswordMatch() {
        const password1 = document.getElementById('id_password1');
        const password2 = document.getElementById('id_password2');
        const matchDiv = document.getElementById('passwordMatch');
        
        if (!password1 || !password2 || !matchDiv) return;

        function checkMatch() {
            if (password2.value.length === 0) {
                matchDiv.innerHTML = '';
                return;
            }
            
            if (password1.value === password2.value) {
                matchDiv.innerHTML = '<span style="color: #28a745;"><i class="fas fa-check-circle me-1"></i>Пароли совпадают</span>';
            } else {
                matchDiv.innerHTML = '<span style="color: #dc3545;"><i class="fas fa-exclamation-circle me-1"></i>Пароли не совпадают</span>';
            }
        }

        password1.addEventListener('input', checkMatch);
        password2.addEventListener('input', checkMatch);
    }

    // Автоматическое скрытие сообщений
    function initAutoHideAlerts() {
        setTimeout(function() {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(alert => {
                alert.style.transition = 'opacity 0.5s';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            });
        }, 5000);
    }

    // Инициализация действий с email
    function initEmailActions() {
        // Подтверждение удаления email
        const deleteForms = document.querySelectorAll('form button[type="submit"][title="Удалить"]');
        deleteForms.forEach(button => {
            const form = button.closest('form');
            if (form) {
                form.addEventListener('submit', function(e) {
                    if (!confirm('Удалить этот email адрес?')) {
                        e.preventDefault();
                    }
                });
            }
        });
    }

    // Экспортируем функции для использования в других файлах
    window.authUtils = {
        showNotification: function(message, type = 'success') {
            const notification = document.createElement('div');
            notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
            notification.style.zIndex = '9999';
            notification.style.maxWidth = '400px';
            notification.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 5000);
        }
    };

})();