// ===== ОСНОВНОЙ JAVASCRIPT ДЛЯ ВСЕГО САЙТА =====

(function() {
    'use strict';

    // Инициализация при загрузке DOM
    document.addEventListener('DOMContentLoaded', function() {
        initAlerts();
        initLogoutConfirmation();
        initTooltips();
        initFormValidation();
    });

    // Автоматическое скрытие alert сообщений через 5 секунд
    function initAlerts() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        if (alerts.length > 0) {
            setTimeout(function() {
                alerts.forEach(function(alert) {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                });
            }, 5000);
        }
    }

    // Подтверждение выхода из аккаунта
    function initLogoutConfirmation() {
        const logoutLinks = document.querySelectorAll('a[href*="logout"]');
        logoutLinks.forEach(function(link) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                showConfirmationDialog(
                    'Выход из аккаунта',
                    'Вы уверены, что хотите выйти?',
                    () => window.location.href = this.href
                );
            });
        });
    }

    // Инициализация Bootstrap tooltips
    function initTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Базовая валидация форм
    function initFormValidation() {
        const forms = document.querySelectorAll('.needs-validation');
        Array.from(forms).forEach(function(form) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }

    // Утилита для показа диалога подтверждения
    window.showConfirmationDialog = function(title, message, onConfirm) {
        if (confirm(`${title}\n\n${message}`)) {
            onConfirm();
        }
    };

    // Утилита для показа уведомления
    window.showNotification = function(message, type = 'success') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show custom-file-notification`;
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    };

    // Утилита для форматирования даты
    window.formatDate = function(date) {
        const d = new Date(date);
        let month = '' + (d.getMonth() + 1);
        let day = '' + d.getDate();
        let year = d.getFullYear();

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;

        return [year, month, day].join('-');
    };

    // Утилита для форматирования телефонного номера
    window.formatPhoneNumber = function(phone) {
        if (!phone) return '';
        let value = phone.replace(/\D/g, '');
        if (value.length > 0) {
            if (value.length <= 1) {
                value = '+7 (' + value;
            } else if (value.length <= 4) {
                value = '+7 (' + value.slice(1, 4);
            } else if (value.length <= 7) {
                value = '+7 (' + value.slice(1, 4) + ') ' + value.slice(4, 7);
            } else if (value.length <= 9) {
                value = '+7 (' + value.slice(1, 4) + ') ' + value.slice(4, 7) + '-' + value.slice(7, 9);
            } else {
                value = '+7 (' + value.slice(1, 4) + ') ' + value.slice(4, 7) + '-' + value.slice(7, 9) + '-' + value.slice(9, 11);
            }
            return value;
        }
        return phone;
    };

})();