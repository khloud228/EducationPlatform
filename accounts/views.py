from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect
from .models import CustomUser
from .forms import ProfileUpdateForm
import os

class ProfileView(LoginRequiredMixin, DetailView):
    """Просмотр профиля пользователя."""
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мой профиль'
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля."""
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context
    
    def delete_avatar_file(self, user):
        """Удаляет файл аватара, если он существует."""
        if user.avatar and hasattr(user.avatar, 'path') and os.path.exists(user.avatar.path):
            # Проверяем, что это не путь к дефолтному аватару
            if 'default' not in user.avatar.name.lower():
                try:
                    os.remove(user.avatar.path)
                    return True
                except Exception as e:
                    print(f"Ошибка при удалении аватара: {e}")
        return False
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        # Проверяем, нужно ли очистить аватар
        if request.POST.get('clear_avatar') == 'true':
            if self.object.avatar:
                # Просто устанавливаем None и сохраняем
                # Сигнал pre_save сам удалит файл
                self.object.avatar = None
                self.object.save()
                messages.success(request, 'Фото профиля удалено')
            return redirect('accounts:profile_edit')
        
        if form.is_valid():
            # Сохраняем форму
            form.save()
            # Сигнал pre_save сам обработает удаление старого файла
            messages.success(self.request, 'Профиль успешно обновлен!')
            return redirect(self.success_url)
        else:
            messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
            return self.form_invalid(form)
    
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
        
    #     # Проверяем, нужно ли удалить аватар
    #     if request.POST.get('clear_avatar') == 'true':
    #         if self.object.avatar:
    #             self.delete_avatar_file(self.object)
    #             self.object.avatar = None
    #             self.object.save()
    #             messages.success(request, 'Фото профиля удалено')
    #         return redirect('accounts:profile')
        
    #     if form.is_valid():
    #         # Проверяем, загружен ли новый файл
    #         if 'avatar' in request.FILES:
    #             # Удаляем старый аватар
    #             if self.object.avatar:
    #                 self.delete_avatar_file(self.object)
    #             # Сохраняем новый
    #             return self.form_valid(form)
    #         else:
    #             # Сохраняем форму без изменения аватара
    #             return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    
        
    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)