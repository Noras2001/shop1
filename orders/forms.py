# orders/forms.py

from django import forms
from .models import Order
from datetime import datetime, time
from django.utils import timezone

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'address',
            'delivery_date',
            'delivery_time',
            'comment',
            'phone',
            'email',
            'payment_method',
        ]
        # Opcionalmente, puedes definir etiquetas (labels) y help_texts
        labels = {
            'address': 'Адрес доставки',
            'delivery_date': 'Дата доставки',
            'delivery_time': 'Время доставки',
            'comment': 'Комментарий',
            'phone': 'Телефон',
            'email': 'Email',
            'payment_method': 'Способ оплаты',
        }
        help_texts = {
            'address': 'Укажите точный адрес доставки',
        }

    def clean_delivery_date(self):
        """
        Valida que la fecha de entrega no sea anterior a hoy.
        """
        delivery_date = self.cleaned_data['delivery_date']
        if delivery_date and delivery_date < timezone.localdate():
            raise forms.ValidationError('Нельзя выбрать дату в прошлом!')
        return delivery_date

    def clean(self):
        """
        Valida coherencia entre fecha y hora, etc.
        """
        cleaned_data = super().clean()
        delivery_date = cleaned_data.get('delivery_date')
        delivery_time = cleaned_data.get('delivery_time')

        # Si ambos existen, validar que no sea pasado
        if delivery_date and delivery_time:
            combined_dt_naive = datetime.combine(delivery_date, delivery_time)
            # Convertir a 'aware' según zona horaria del proyecto
            combined_dt = timezone.make_aware(
                combined_dt_naive,
                timezone.get_current_timezone()
            )
            now = timezone.now()

            if combined_dt < now:
                # Forzar error a nivel de formulario
                self.add_error('delivery_date', 'Нельзя выбрать прошедшую дату/время!')
                self.add_error('delivery_time', 'Нельзя выбрать прошедшую дату/время!')

        return cleaned_data
