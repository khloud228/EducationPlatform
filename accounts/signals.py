from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(pre_save, sender=CustomUser)
def set_username_from_email(sender, instance, **kwargs):
    """Сигнал для установки username из email перед сохранением."""
    if not instance.username:
        instance.username = CustomUser.objects.generate_username_from_email(instance.email)