from django.http import JsonResponse
from aiogram import Bot, types
import asyncio
import os

# Token y chat ID
TELEGRAM_BOT_TOKEN = '8142502168:AAGxuFLlmu_oFeG23TV4W4nV9yg6VTL8Va4'
CHAT_ID = '1109953581'

# Ruta base de las imágenes
BASE_IMAGE_PATH = r'D:\shop1\catalog\static\catalog\img'


# Función para enviar mensajes
async def enviar_mensaje(chat_id, mensaje):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_message(chat_id=chat_id, text=mensaje, parse_mode=types.ParseMode.MARKDOWN)
    finally:
        await bot.close()


# Función para enviar fotos
async def enviar_foto(chat_id, foto_path, caption=""):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        with open(foto_path, 'rb') as foto:
            await bot.send_photo(chat_id=chat_id, photo=foto, caption=caption)
    except Exception as e:
        print(f"Error al enviar la foto {foto_path}: {e}")
    finally:
        await bot.close()


# Vista para manejar pedidos
def new_order(request):
    if request.method == 'POST':
        try:
            data = request.json
            bouquets = data.get('bouquets', [])
            total = data.get('total', 0)
            fecha = data.get('delivery_date', 'No especificado')
            hora = data.get('delivery_time', 'No especificado')
            direccion = data.get('delivery_address', 'No especificado')
            comentarios = data.get('comments', 'Sin comentarios')

            # Crear mensaje inicial
            mensaje = (
                f"📦 *Новый заказ*:\n\n"
                f"💐 Букеты:\n"
                f"{''.join([f'- {b['name']} - {b['price']} ₽\n' for b in bouquets])}"
                f"💰 Общая сумма: {total} ₽\n"
                f"📅 Дата доставки: {fecha}\n"
                f"⏰ Время доставки: {hora}\n"
                f"📍 Адрес доставки: {direccion}\n"
                f"✍️ Комментарии: {comentarios}"
            )

            # Enviar mensaje principal
            asyncio.run(enviar_mensaje(CHAT_ID, mensaje))

            # Enviar fotos de los productos
            for bouquet in bouquets:
                image_path = os.path.join(BASE_IMAGE_PATH, bouquet.get('image_path', '').lstrip('/'))
                caption = f"{bouquet['name']} - {bouquet['price']} ₽"

                # Log para depurar la ruta de la imagen
                print(f"Procesando imagen: {image_path}")

                if os.path.exists(image_path):
                    asyncio.run(enviar_foto(CHAT_ID, image_path, caption))
                else:
                    print(f"⚠️ Imagen no encontrada: {image_path}")

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            print(f"Error al procesar el pedido: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'}, status=405)

