from django.db import models
from django.conf import settings
from catalog.models import Product

from django.db import models
from django.conf import settings




class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, blank=True)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_time = models.TimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)  # Teléfono
    email = models.EmailField(blank=True, null=True)  # Email
    payment_method = models.CharField(max_length=50, blank=True)  # Método de pago (tarjeta, efectivo, etc.)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

