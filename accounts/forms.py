from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
import os

class CustomUserCreationForm(UserCreationForm):
    """Форма для создания пользователя (регистрация)."""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

class CustomUserChangeForm(UserChangeForm):
    """Форма для изменения пользователя (админка)."""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'avatar', 'bio', 
                  'phone', 'date_of_birth', 'city')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'style': 'background-color: #f8f9fa;'
            }),
        }

class ProfileUpdateForm(forms.ModelForm):
    """Форма для обновления профиля пользователем."""
    
    # Скрытое поле для отслеживания удаления аватара
    clear_avatar = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'avatar', 'bio', 
                  'phone', 'date_of_birth', 'city')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите вашу фамилию'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Расскажите о себе...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш город'
            }),
            # НЕ скрываем avatar, а делаем его кастомным в шаблоне
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем стандартные подписи, но оставляем поле видимым для Django
        self.fields['avatar'].required = False
        self.fields['avatar'].label = 'Фото профиля'
        self.fields['avatar'].help_text = 'Форматы: JPG, PNG, GIF, WebP. Максимум 2MB.'
        
        # Устанавливаем формат даты для отображения
        if self.instance and self.instance.date_of_birth:
            self.initial['date_of_birth'] = self.instance.date_of_birth.strftime('%Y-%m-%d')
    
    def clean_avatar(self):
        """Валидация загружаемого аватара."""
        avatar = self.cleaned_data.get('avatar')
        
        # Если avatar пустой или это не новый файл, пропускаем валидацию
        if not avatar or isinstance(avatar, str):
            return avatar
        
        # Проверка размера файла (2MB)
        if avatar.size > 2 * 1024 * 1024:
            raise forms.ValidationError('Размер файла не должен превышать 2MB.')
        
        # Проверка типа файла
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        ext = os.path.splitext(avatar.name)[1].lower()
        if ext not in valid_extensions:
            raise forms.ValidationError('Поддерживаются только форматы: JPG, JPEG, PNG, GIF, WebP.')
        
        return avatar