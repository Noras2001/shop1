from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    #  Показать 'phone' в списке
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')

    #  Добавьте 'phone' в форму редактирования
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('phone',)
        }),
    )

