# user\models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя, унаследованная от AbstractUser.
    Добавлены дополнительные поля: телефон, адрес, email и метод оплаты.
    """
    phone = models.CharField(
        'Телефон', max_length=20, blank=True, null=True,
        validators=[RegexValidator(
            regex=r'^\+?\d{7,15}$',
            message='Номер телефона должен содержать от 7 до 15 цифр (может включать +).'
        )]
    )
    address = models.CharField('Адрес', max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    

    def __str__(self):
        return self.username


