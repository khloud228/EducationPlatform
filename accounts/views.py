from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from .models import CustomUser
from .forms import ProfileUpdateForm
from django.contrib import messages
from django.shortcuts import redirect


class ProfileView(LoginRequiredMixin, DetailView):
    """Просмотр профиля пользователя."""
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        # Возвращаем текущего пользователя
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
        # Редактируем профиль текущего пользователя
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context
    
    def form_valid(self, form):
        """Если форма валидна, сохраняем и показываем сообщение."""
        # Обработка удаления аватара
        if self.request.POST.get('remove_avatar'):
            user = self.get_object()
            if user.avatar:
                user.avatar.delete()
                user.avatar = None
                user.save()
                messages.success(self.request, 'Аватар успешно удален!')
                return redirect(self.success_url)
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)