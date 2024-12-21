from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'available', 'image')  # Añade 'image' para mostrarla
    list_filter = ('available', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'available')  # Para edición rápida en la lista
    fields = ('name', 'slug', 'category', 'description', 'price', 'stock', 'available', 'image')  # Incluye 'image'





