# shop1/orders/views.py
import asyncio
import os
from dotenv import load_dotenv
import logging
from .models import Order, OrderItem
from user.models import CustomUser
from cart.models import Cart
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode


# Настройка логирования
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@login_required
def create_order(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or cart.items.count() == 0:
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user

            # Рассчитайте общую сумму
            total = 0
            for item in cart.items.select_related('product'):
                total += item.product.price * item.quantity
            order.total = total
            order.save()

            # Создание OrderItems с изображением товара
            for item in cart.items.select_related('product'):
                if item.product.image:
                    image_url = item.product.image.url
                else:
                    image_url = ''
                print(f"Создание OrderItem: Producto={item.product.name}, Imagen={image_url}")  # Debug
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    product_image=image_url  # Сохранить URL-адрес изображения
                )

            # Очистить корзину после создания заказа
            cart.items.all().delete()

            return redirect('orders:order_confirm', order_id=order.id)
        else:
            return render(request, 'orders/order_form.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'orders/order_form.html', {'form': form})

async def send_telegram_notification(order):
    """ Отправка уведомления о заказе в Telegram с изображениями."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError("TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не настроены")

    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Формат сообщения с информацией о заказе
    message = (
        f"📦 Новый заказ #{order.id}!\n"
        f"📍 Адрес доставки: {order.address}\n"        
        f"📅 Дата: {order.delivery_date}\n"
        f"⏰ Время: {order.delivery_time}\n"
        f"✍️ Комментарий: {order.comment or 'нет'}\n"
        f"💰 Сумма: {order.total:.2f} руб.\n"
        f"📞 Телефон: {order.user.phone}\n"
        f"📧 Email: {order.user.email}\n"
        f"Способ оплаты: {order.payment_method}\n"
    )

    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


@login_required
def order_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        order.is_confirmed = True
        order.save()

        try:
            asyncio.run(send_telegram_notification(order))
        except Exception as e:
            print(f"Ошибка при отправке уведомления: {e}")

        return redirect('orders:order_success', order_id=order.id)

    return render(request, 'orders/order_confirm.html', {'order': order})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})
