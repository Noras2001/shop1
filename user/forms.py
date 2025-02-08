# user\forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
import re

class CustomUserCreationForm(UserCreationForm):
    # Добавляем поле для ввода номера телефона
    phone = forms.CharField(
        max_length=13,  # Максимальная длина (код страны +7 и 10 цифр)
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Телефон (+7...)'}),  # Место для ввода номера телефона
    )

    def clean_phone(self):
        # Получаем введенный номер телефона
        phone = self.cleaned_data.get('phone')
        
        # Проверяем, начинается ли номер с кода страны +7
        if not phone.startswith('+7'):
            raise ValidationError('Номер должен начинаться с кода страны +7.')
        
        # Удаляем код страны (+7) и проверяем, что остаются только 10 цифр
        phone = phone[2:]  # Убираем '+7'
        if len(phone) != 10 or not phone.isdigit():
            raise ValidationError('Номер должен содержать ровно 10 цифр после +7.')
        
        # Возвращаем номер с кодом страны
        return '+7' + phone

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password1', 'password2')
