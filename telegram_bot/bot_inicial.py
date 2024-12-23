import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

# FlowerDelivery_shop10_bot

bot = Bot(token='8142502168:AAGxuFLlmu_oFeG23TV4W4nV9yg6VTL8Va4')
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())