from .models import Order, OrderItem
from cart.models import Cart
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio
import os
from dotenv import load_dotenv

# Cargar variables de entorno
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

            # Calcular total
            total = 0
            for item in cart.items.select_related('product'):
                total += item.product.price * item.quantity
            order.total = total
            order.save()

            # Crear OrderItems
            for item in cart.items.select_related('product'):
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            return redirect('orders:order_confirm', order_id=order.id)
        else:
            return render(request, 'orders/order_form.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'orders/order_form.html', {'form': form})


async def send_telegram_notification(order):
    """
    Enviar notificación del pedido por Telegram.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError("El TOKEN o el CHAT_ID no están configurados.")

    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Formatea el mensaje con la información del pedido
    message = (
        f"Новый заказ #{order.id}!\n"
        f"Адрес доставки: {order.address}\n"        
        f"Дата: {order.delivery_date}\n"
        f"Время: {order.delivery_time}\n"
        f"Комментарий: {order.comment}\n"
        f"Сумма: {order.total:.2f} руб.\n"
        f"Телефон: {order.phone}\n"
        f"Email: {order.email}\n"
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
            print(f"Error enviando notificación: {e}")

        return redirect('orders:order_success', order_id=order.id)

    return render(request, 'orders/order_confirm.html', {'order': order})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})
