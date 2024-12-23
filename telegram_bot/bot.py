import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import InputFile
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import InputFile
from api import app  # Importar la app de FastAPI
import uvicorn



# Reemplaza 'YOUR_BOT_TOKEN' con el token que obtuviste de BotFather
BOT_TOKEN = '8142502168:AAGxuFLlmu_oFeG23TV4W4nV9yg6VTL8Va4'

# Reemplaza con el ID de chat donde quieres recibir los pedidos
CHAT_ID = '1109953581'

# Inicializar el bot y el dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def send_order(order):
    """
    Función para enviar el pedido a Telegram.
    :param order: Diccionario con detalles del pedido
    """
    try:
        # Construir el mensaje
        message = f"📦 **Nuevo Pedido Recibido** 📦\n\n"
        message += f"**Bouquet(s):**\n"
        for bouquet in order['bouquets']:
            message += f"• {bouquet['name']} - ${bouquet['price']}\n"
        message += f"\n**Costo Total:** ${order['total']}\n"
        message += f"**Fecha de Entrega:** {order['delivery_date']}\n"
        message += f"**Hora de Entrega:** {order['delivery_time']}\n"
        message += f"**Lugar de Entrega:** {order['delivery_address']}\n"
        if order.get('comments'):
            message += f"**Comentarios:** {order['comments']}\n"

        # Enviar el mensaje
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')

        # Enviar imágenes de los bouquets
        for bouquet in order['bouquets']:
            if bouquet.get('image_path'):
                photo = InputFile(bouquet['image_path'])
                await bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=bouquet['name'])

        print("Pedido enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el pedido: {e}")

async def run_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # Correr el bot y la API en paralelo
    await asyncio.gather(
        dp.start_polling(bot),
        run_api(),
    )

if __name__ == '__main__':
    asyncio.run(main())