from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_image_display',)
    fields = ('product', 'quantity', 'price', 'product_image_display')

    def product_image_display(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" width="100" />', obj.product_image)
        return "No Image"
    product_image_display.short_description = 'Изображение'




class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total', 'is_confirmed')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)


