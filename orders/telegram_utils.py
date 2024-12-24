# orders/telegram_utils.py

import os
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from django.conf import settings
from dotenv import load_dotenv
from asgiref.sync import async_to_sync
import asyncio

# Cargar variables de entorno
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("El TOKEN o el CHAT_ID no están configurados en las variables de entorno.")

# Ruta base de las imágenes
BASE_IMAGE_PATH = os.path.join(settings.BASE_DIR, 'catalog', 'static', 'catalog', 'img')

# Variable global para el bot
bot = None

def get_bot():
    global bot
    if bot is None:
        bot = Bot(
            token=TELEGRAM_BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        print("Bot inicializado correctamente.")
    return bot

async def enviar_mensaje(chat_id: str, mensaje: str):
    """
    Enviar un mensaje de texto al chat de Telegram.
    """
    try:
        print(f"Enviando mensaje a {chat_id}: {mensaje}")
        await get_bot().send_message(chat_id=chat_id, text=mensaje, parse_mode=ParseMode.MARKDOWN)
        print("Mensaje enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")

async def enviar_foto(chat_id: str, foto_path: str, caption: str = ""):
    """
    Enviar una foto al chat de Telegram con un pie de foto opcional.
    """
    try:
        print(f"Enviando foto a {chat_id}: {foto_path} con caption: {caption}")
        with open(foto_path, 'rb') as foto:
            await get_bot().send_photo(chat_id=chat_id, photo=foto, caption=caption, parse_mode=ParseMode.MARKDOWN)
        print("Foto enviada exitosamente.")
    except FileNotFoundError:
        error_mensaje = f"⚠️ **Imagen no encontrada:** `{foto_path}`"
        print(error_mensaje)
        await enviar_mensaje(chat_id, error_mensaje)
    except Exception as e:
        print(f"Error al enviar la foto {foto_path}: {e}")
        error_mensaje = f"⚠️ **Error al enviar la imagen:** `{foto_path}`"
        await enviar_mensaje(chat_id, error_mensaje)

async def send_telegram_notification(order):
    """
    Enviar notificación del pedido por Telegram, incluyendo fotos de los productos.
    """
    mensaje = (
        f"📦 *Nuevo Pedido* #{order.id}\n"
        f"💐 *Productos:*\n"
    )

    # Construir la lista de productos
    for item in order.items.all():
        mensaje += f"• {item.product.name} x{item.quantity} - {item.price} ₽\n"

    mensaje += (
        f"\n💰 *Total:* {order.total} ₽\n"
        f"📅 *Fecha de Entrega:* {order.delivery_date}\n"
        f"⏰ *Hora de Entrega:* {order.delivery_time}\n"
        f"📍 *Dirección:* {order.address}\n"
        f"📞 *Teléfono:* {order.phone}\n"
        f"📧 *Email:* {order.email}\n"
        f"✍️ *Comentarios:* {order.comment or 'Ninguno'}"
    )

    # Enviar el mensaje principal
    await enviar_mensaje(TELEGRAM_CHAT_ID, mensaje)

    # Enviar fotos de los productos
    for item in order.items.all():
        if item.product.image:
            image_path = os.path.join(BASE_IMAGE_PATH, item.product.image.name)
            caption = f"{item.product.name} - {item.price} ₽"
            print(f"Enviando imagen: {image_path}")
            await enviar_foto(TELEGRAM_CHAT_ID, image_path, caption)
        else:
            aviso = f"⚠️ *No hay imagen disponible para:* `{item.product.name}`"
            await enviar_mensaje(TELEGRAM_CHAT_ID, aviso)

# Función de prueba
async def send_test_message():
    """
    Enviar un mensaje de prueba a Telegram.
    """
    try:
        await enviar_mensaje(TELEGRAM_CHAT_ID, "Mensaje de prueba desde Django.")
        print("Mensaje de prueba enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el mensaje de prueba: {e}")
