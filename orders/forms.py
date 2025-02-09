from django import forms
from .models import Order
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'delivery_date', 'delivery_time', 'comment']

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы для подтягивания номера телефона пользователя
        если он уже залогинен.
        """
        super().__init__(*args, **kwargs)
        # Проверяем, если пользователь залогинен
        if self.user_is_authenticated():
            user = self.get_authenticated_user()
            # Если номер телефона есть у пользователя, подтягиваем его в форму
            if user.phone:
                self.fields['phone'].initial = user.phone
            self.fields['phone'].required = True
            self.fields['address'].required = True
            self.fields['delivery_time'].required = True

    def user_is_authenticated(self):
        """Проверка, залогинен ли пользователь."""
        return hasattr(self, 'user') and self.user.is_authenticated

    def get_authenticated_user(self):
        """Получаем залогированного пользователя."""
        return get_user_model().objects.get(username=self.user.username)

    def clean_delivery_date(self):
        """
        Убедитесь, что дата доставки - не раньше сегодняшнего дня.
        """
        delivery_date = self.cleaned_data['delivery_date']
        if delivery_date and delivery_date < timezone.localdate():
            raise forms.ValidationError('Нельзя выбрать дату в прошлом!')
        return delivery_date

    def clean(self):
        """
        Проверяет соответствие между датой и временем и т.д.
        """
        cleaned_data = super().clean()
        delivery_date = cleaned_data.get('delivery_date')
        delivery_time = cleaned_data.get('delivery_time')

        # Если оба варианта существуют:
        if delivery_date and delivery_time:
            combined_dt_naive = datetime.combine(delivery_date, delivery_time)
            # Преобразование в 'aware' в соответствии с часовым поясом проекта
            combined_dt = timezone.make_aware(
                combined_dt_naive,
                timezone.get_current_timezone()
            )
            now = timezone.now()

            if combined_dt < now:
                # Принудительная ошибка на уровне формы
                self.add_error('delivery_date', 'Нельзя выбрать прошедшую дату/время!')
                self.add_error('delivery_time', 'Нельзя выбрать прошедшую дату/время!')

        return cleaned_data
