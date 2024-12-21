from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    #  Mostrar 'phone' en la lista
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')

    #  Agregar 'phone' en el formulario de edición (en la sección de “Información Personal” o similar)
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('phone',)
        }),
    )

