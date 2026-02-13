"""
Django settings for educational_portfolio project.
"""

import os
from pathlib import Path

# ========== БАЗОВЫЕ НАСТРОЙКИ ==========

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'
DEBUG = True
ALLOWED_HOSTS = []


# ========== ПРИЛОЖЕНИЯ ==========

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'crispy_bootstrap5',
    
    'accounts',
    'core',
]


# ========== MIDDLEWARE ==========

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'


# ========== ШАБЛОНЫ ==========

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ========== БАЗА ДАННЫХ ==========

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ========== ВАЛИДАЦИЯ ПАРОЛЕЙ ==========

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ========== ИНТЕРНАЦИОНАЛИЗАЦИЯ ==========

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


# ========== СТАТИЧЕСКИЕ ФАЙЛЫ ==========

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ========== КАСТОМНАЯ МОДЕЛЬ ПОЛЬЗОВАТЕЛЯ ==========

AUTH_USER_MODEL = 'accounts.CustomUser'


# ========== DJANGO-ALLAUTH НАСТРОЙКИ ==========

SITE_ID = 1

# ----- МЕТОДЫ АУТЕНТИФИКАЦИИ -----
ACCOUNT_LOGIN_METHODS = {'email'}

# ----- НАСТРОЙКИ РЕГИСТРАЦИИ -----
ACCOUNT_SIGNUP_FIELDS = [
    'email*',
    'password1*',
    'password2*',
    'first_name',
    'last_name',
]

# ----- НАСТРОЙКИ EMAIL -----
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_UNIQUE_EMAIL = True

# ----- НАСТРОЙКИ ВХОДА/ВЫХОДА -----
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGIN_URL = 'account_login'
LOGOUT_REDIRECT_URL = 'core:home'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_SESSION_REMEMBER = True

# ----- НАСТРОЙКИ БЕЗОПАСНОСТИ -----
ACCOUNT_PASSWORD_MIN_LENGTH = 8

# ----- ОГРАНИЧЕНИЕ ПОПЫТОК -----
# ACCOUNT_RATE_LIMITS = {
#     'login_failed': '5/300',
#     'signup': '5/3600',
#     'password_reset': '5/3600',
# }


# ========== АУТЕНТИФИКАЦИЯ ==========

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


# ========== CRISPY FORMS ==========

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# ========== EMAIL ==========

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ========== ПЕРВИЧНЫЙ КЛЮЧ ==========

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ========== ЛОГИРОВАНИЕ ==========

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'INFO',
#     },
# }