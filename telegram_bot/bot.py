import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties

# Carga del token desde .env
from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Inicialización del bot con propiedades predeterminadas
bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    session=AiohttpSession(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Crear Router
router = Router()


# Handler de comandos
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Привет! Я ваш бот для магазина цветов. Чем могу помочь?")


async def main():
    # Crear Dispatcher
    dp = Dispatcher()

    # Registrar el router
    dp.include_router(router)

    # Configuración del bot
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
