from aiogram import Bot, types
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def get_chat_id():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    updates = await bot.get_updates()
    for update in updates:
        if update.message:
            print(f"CHAT_ID: {update.message.chat.id}")
    await bot.session.close()

asyncio.run(get_chat_id())
