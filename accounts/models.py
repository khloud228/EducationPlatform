from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class CustomUserManager(BaseUserManager):
    """Кастомный менеджер для модели пользователя с автоматическим username из email."""
    
    def generate_username_from_email(self, email):
        """Генерирует username из части email до @."""
        username = email.split('@')[0]
        
        # Транслитерация и очистка
        username = slugify(username)
        
        # Если после транслитерации пусто, используем базовое имя
        if not username:
            username = 'user'
        
        # Проверяем уникальность
        base_username = username
        counter = 1
        while self.model.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
            
        return username
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError('Email должен быть указан')
        
        email = self.normalize_email(email)
        
        # Генерируем username из email, если не указан
        if 'username' not in extra_fields or not extra_fields['username']:
            extra_fields['username'] = self.generate_username_from_email(email)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя с email в качестве идентификатора,
    но username генерируется автоматически из email.
    """
    # Делаем email уникальным и обязательным
    email = models.EmailField(_('email address'), unique=True)
    
    # username оставляем, но он будет генерироваться автоматически
    # и может быть скрыт от пользователя
    
    # Дополнительные поля
    avatar = models.ImageField(
        _('аватар'), 
        upload_to='avatars/', 
        blank=True, 
        null=True
    )
    bio = models.TextField(_('о себе'), max_length=500, blank=True)
    phone = models.CharField(_('телефон'), max_length=20, blank=True)
    date_of_birth = models.DateField(_('дата рождения'), null=True, blank=True)
    city = models.CharField(_('город'), max_length=100, blank=True)
    
    # Даты
    created_at = models.DateTimeField(_('дата регистрации'), auto_now_add=True)
    updated_at = models.DateTimeField(_('дата обновления'), auto_now=True)
    
    # Указываем менеджер
    objects = CustomUserManager()
    
    # Поле для аутентификации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # email и password всегда запрашиваются, остальное опционально
    
    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} ({self.username})"
    
    def get_full_name(self):
        """Возвращает полное имя пользователя."""
        if self.first_name and self.last_name:
            return f"{self.last_name} {self.first_name}"
        return self.email
    
    def get_short_name(self):
        """Возвращает короткое имя (имя, username или email)."""
        if self.first_name:
            return self.first_name
        return self.username
    
    @property
    def has_avatar(self):
        """Проверяет, есть ли у пользователя аватар."""
        return bool(self.avatar) and hasattr(self.avatar, 'url')
    
    def save(self, *args, **kwargs):
        """Генерируем username при сохранении, если его нет."""
        if not self.username:
            self.username = CustomUserManager.generate_username_from_email(self, self.email)
        super().save(*args, **kwargs)