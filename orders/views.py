# shop1/orders/views.py
import os
import logging
from dotenv import load_dotenv
import telebot
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Order, OrderItem
from user.models import CustomUser
from cart.models import Cart
from .forms import OrderForm

# Настройка логирования
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Инициализация Telebot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

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
            total = sum(item.product.price * item.quantity for item in cart.items.select_related('product'))
            order.total = total
            order.save()

            # Создание OrderItems с изображением товара
            for item in cart.items.select_related('product'):
                image_url = item.product.image.url if item.product.image else ''
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    product_image=image_url
                )

            # Очистить корзину после создания заказа
            cart.items.all().delete()

            return redirect('orders:order_confirm', order_id=order.id)
        else:
            return render(request, 'orders/order_form.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'orders/order_form.html', {'form': form})

def send_telegram_notification(order):
    """ Отправка уведомления о заказе в Telegram с изображениями."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не настроены")
        return

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

    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления в Telegram: {e}")

@login_required
def order_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        order.is_confirmed = True
        order.save()

        try:
            send_telegram_notification(order)
        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления: {e}")

        return redirect('orders:order_success', order_id=order.id)

    return render(request, 'orders/order_confirm.html', {'order': order})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})
