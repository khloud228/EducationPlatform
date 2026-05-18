from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import CustomUser
import os


@receiver(pre_save, sender=CustomUser)
def set_username_from_email(sender, instance, **kwargs):
    """Сигнал для установки username из email перед сохранением."""
    if not instance.username:
        instance.username = CustomUser.objects.generate_username_from_email(instance.email)


@receiver(pre_save, sender=CustomUser)
def delete_old_avatar_on_change(sender, instance, **kwargs):
    """
    Удаляет старый файл аватара при загрузке нового.
    Срабатывает перед сохранением в БД.
    """
    # Если это новый пользователь (нет id), ничего не делаем
    if not instance.pk:
        return
    
    try:
        # Получаем старую версию пользователя из БД
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    
    # Проверяем, изменился ли аватар
    old_avatar = old_instance.avatar
    new_avatar = instance.avatar
    
    # Если аватар изменился и старый существовал
    if old_avatar and old_avatar != new_avatar:
        # Получаем путь к файлу
        if hasattr(old_avatar, 'path') and os.path.exists(old_avatar.path):
            # Проверяем, что это не дефолтный аватар
            if 'default' not in old_avatar.name.lower():
                try:
                    os.remove(old_avatar.path)
                    print(f"Сигнал: старый аватар удален: {old_avatar.path}")
                except Exception as e:
                    print(f"Сигнал: ошибка при удалении старого аватара: {e}")
    
    # Если аватар был удален (старый был, новый None)
    elif old_avatar and not new_avatar:
        if hasattr(old_avatar, 'path') and os.path.exists(old_avatar.path):
            if 'default' not in old_avatar.name.lower():
                try:
                    os.remove(old_avatar.path)
                    print(f"Сигнал: аватар удален (очистка поля): {old_avatar.path}")
                except Exception as e:
                    print(f"Сигнал: ошибка при удалении аватара: {e}")

@receiver(post_delete, sender=CustomUser)
def delete_avatar_on_user_delete(sender, instance, **kwargs):
    """Удаляет файл аватара при удалении пользователя."""
    if instance.avatar and hasattr(instance.avatar, 'path') and os.path.exists(instance.avatar.path):
        if 'default' not in instance.avatar.name.lower():
            try:
                os.remove(instance.avatar.path)
                print(f"Аватар удален при удалении пользователя: {instance.avatar.path}")
            except Exception as e:
                print(f"Ошибка при удалении аватара при удалении пользователя: {e}")