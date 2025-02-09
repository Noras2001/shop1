#\orders\models.py

from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from catalog.models import Product

class Order(models.Model):
    """
    Модель заказа, содержащая информацию о пользователе, статусе и общей сумме.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.CharField('Адрес', max_length=255, blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_time = models.TimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    """
    Модель товара в заказе. Хранит связь с заказом и конкретным продуктом,
    а также информацию о количестве и цене.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='order_item_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"





