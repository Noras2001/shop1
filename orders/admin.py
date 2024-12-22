from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'delivery_date', 'is_confirmed')
    list_filter = ('is_confirmed', 'delivery_date')

