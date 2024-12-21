from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Модель пользователя, унаследованная от AbstractUser.
    Добавляем дополнительные поля, если нужно.
    """
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

