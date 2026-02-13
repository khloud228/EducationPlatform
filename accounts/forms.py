# from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):
#     """Форма для создания пользователя (регистрация) - username скрыт."""
    
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'first_name', 'last_name')
#         widgets = {
#             'email': forms.EmailInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Введите ваш email'
#             }),
#             'first_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Имя'
#             }),
#             'last_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Фамилия'
#             }),
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Скрываем поле username, так как оно генерируется автоматически
#         if 'username' in self.fields:
#             del self.fields['username']
    
#     def clean_email(self):
#         """Валидация email."""
#         email = self.cleaned_data.get('email')
#         if CustomUser.objects.filter(email=email).exists():
#             raise forms.ValidationError('Пользователь с таким email уже существует')
#         return email

# class CustomUserChangeForm(UserChangeForm):
#     """Форма для изменения пользователя (админка)."""
    
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'username', 'first_name', 'last_name', 'avatar', 'bio', 
#                   'phone', 'date_of_birth', 'city')
#         widgets = {
#             'username': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'readonly': 'readonly',  # Только для чтения в админке
#                 'style': 'background-color: #f8f9fa;'
#             }),
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Добавляем подсказку для поля username
#         self.fields['username'].help_text = 'Генерируется автоматически из email'
#         self.fields['username'].required = False

# class ProfileUpdateForm(forms.ModelForm):
#     """Форма для обновления профиля пользователем - username не показываем."""
    
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'avatar', 'bio', 
#                   'phone', 'date_of_birth', 'city')
#         widgets = {
#             'first_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Введите ваше имя'
#             }),
#             'last_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Введите вашу фамилию'
#             }),
#             'bio': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 4,
#                 'placeholder': 'Расскажите о себе...'
#             }),
#             'phone': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': '+7 (999) 123-45-67'
#             }),
#             'date_of_birth': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'type': 'date'
#             }),
#             'city': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Ваш город'
#             }),
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['avatar'].required = False
#         self.fields['avatar'].help_text = 'Загрузите фото профиля (JPEG, PNG до 2MB)'
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Форма для создания пользователя (регистрация) - username скрыт."""
    
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Генерируется автоматически из email'
        self.fields['username'].required = False

class ProfileUpdateForm(forms.ModelForm):
    """Форма для обновления профиля пользователем."""
    
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
                'style': 'font-family: inherit;'  # Убираем моноширинный шрифт
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш город'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].required = False
        self.fields['avatar'].help_text = 'Загрузите фото профиля (JPEG, PNG до 2MB)'
        
        # Устанавливаем формат даты для отображения
        if self.instance and self.instance.date_of_birth:
            # Преобразуем дату в формат YYYY-MM-DD для input type="date"
            self.initial['date_of_birth'] = self.instance.date_of_birth.strftime('%Y-%m-%d')