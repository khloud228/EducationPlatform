from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    # Поля для отображения в списке пользователей
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_display_links = ('email', 'username')
    list_filter = ('is_staff', 'is_active', 'created_at', 'city')
    
    # Поля для редактирования в админке
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Персональная информация'), {
            'fields': ('first_name', 'last_name', 'avatar', 'bio', 
                      'phone', 'date_of_birth', 'city')
        }),
        (_('Права доступа'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 
                      'groups', 'user_permissions'),
        }),
        (_('Важные даты'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    # Поля при создании нового пользователя в админке
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 
                      'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    
    # Поиск и сортировка
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('username', 'created_at', 'updated_at')  # username только для чтения
    
    def get_readonly_fields(self, request, obj=None):
        """Делаем username только для чтения при редактировании."""
        if obj:  # Редактирование существующего пользователя
            return self.readonly_fields + ('username',)
        return self.readonly_fields