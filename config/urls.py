from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),
    
    # Allauth (аутентификация)
    path('accounts/', include('allauth.urls')),
    
    # Наши приложения
    path('', include('core.urls', namespace='core')),
    path('profile/', include('accounts.urls', namespace='accounts')),
]

# Обслуживание медиафайлов в разработке
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)