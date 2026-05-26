import asyncio
import time
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

SPAM_TIMEOUT = 120

bot = Bot(token=TOKEN)
dp = Dispatcher()

last_message_time = {}

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Это анонимная предложка.\n"
        "Пиши сюда сообщения — я их получу.\n\n"
        "🔒 Полная анонимность."
    )

@dp.message(F.text)
async def handler(message: Message):
    user_id = message.from_user.id
    now = time.time()

    if user_id in last_message_time:
        if now - last_message_time[user_id] < SPAM_TIMEOUT:
            await message.answer("⏳ Подожди перед следующим сообщением.")
            return

    last_message_time[user_id] = now

    await bot.send_message(
        ADMIN_ID,
        f"📩 Анонимное сообщение:\n\n{message.text}"
    )

    await message.answer("✅ Отправлено!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())