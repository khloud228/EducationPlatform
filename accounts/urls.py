from django.urls import path, re_path
from . import views
from allauth.account.views import (
    LoginView, SignupView, LogoutView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetFromKeyView, PasswordResetFromKeyDoneView,
    EmailView, ConfirmEmailView, EmailVerificationSentView,
    AccountInactiveView, PasswordChangeView, PasswordSetView
)


app_name = 'accounts'

urlpatterns = [
    # Переопределяем страницы аутентификации с указанием наших шаблонов
    path('login/', 
         LoginView.as_view(template_name='accounts/login.html'), 
         name='login'),
    
    path('signup/', 
         SignupView.as_view(template_name='accounts/signup.html'), 
         name='signup'),
    
    path('logout/', 
         LogoutView.as_view(template_name='accounts/logout.html'), 
         name='logout'),
    
    path('password/reset/', 
         PasswordResetView.as_view(template_name='accounts/password_reset.html'), 
         name='reset_password'),
    
    path('password/reset/done/', 
         PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), 
         name='reset_password_done'),
    
    re_path(r'^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
         PasswordResetFromKeyView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='reset_password_from_key'),
    
    path('password/reset/key/done/',
         PasswordResetFromKeyDoneView.as_view(template_name='accounts/password_reset_complete.html'),
         name='reset_password_from_key_done'),
    
    path('confirm-email/',
         EmailVerificationSentView.as_view(template_name='accounts/verification_sent.html'),
         name='email_verification_sent'),
    
    re_path(r'^confirm-email/(?P<key>[-:\w]+)/$',
         ConfirmEmailView.as_view(template_name='accounts/email_confirm.html'),
         name='confirm_email'),
    
    path('inactive/',
         AccountInactiveView.as_view(template_name='accounts/account_inactive.html'),
         name='inactive'),
    
    # Управление email
    path('email/',
         EmailView.as_view(template_name='accounts/email.html'),
         name='email'),
    
    # Смена пароля
    path('password/change/',
         PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='change_password'),
    
    path('password/set/',
         PasswordSetView.as_view(template_name='accounts/password_set.html'),
         name='set_password'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
]