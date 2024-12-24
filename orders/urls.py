# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('confirm/<int:order_id>/', views.order_confirm, name='order_confirm'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
]