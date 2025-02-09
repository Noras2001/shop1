# user\admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Настройка отображения модели CustomUser в админке.
    """
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('phone', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('phone', 'address')}),
    )
    list_display = ('username', 'email', 'phone', 'address', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)


