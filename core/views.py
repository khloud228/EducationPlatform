from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class HomeView(TemplateView):
    """Главная страница."""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

class AboutView(TemplateView):
    """Страница 'О нас'."""
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О платформе'
        return context

class ContactView(TemplateView):
    """Страница контактов."""
    template_name = 'core/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context

class PrivacyPolicyView(TemplateView):
    """Политика конфиденциальности."""
    template_name = 'core/privacy.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Политика конфиденциальности'
        return context

class TermsOfServiceView(TemplateView):
    """Условия использования."""
    template_name = 'core/terms.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Условия использования'
        return context

class DashboardView(LoginRequiredMixin, TemplateView):
    """Личный кабинет (дашборд)."""
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        context['user'] = self.request.user
        
        # Здесь позже добавим статистику и курсы
        context['welcome_message'] = f'Добро пожаловать, {self.request.user.get_short_name()}!'
        
        return context