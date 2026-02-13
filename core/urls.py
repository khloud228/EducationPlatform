from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    # path('contact/', views.ContactView.as_view(), name='contact'),
    # path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy'),
    # path('terms/', views.TermsOfServiceView.as_view(), name='terms'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]