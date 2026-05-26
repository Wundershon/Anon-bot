import asyncio
import time
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

last_message_time = {}
COOLDOWN = 120

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привет 👋\n\nПросто напиши сообщение, и оно будет доставлено."
    )

@dp.message()
async def handle(message: types.Message):
    user_id = message.from_user.id
    now = time.time()

    if user_id in last_message_time:
        if now - last_message_time[user_id] < COOLDOWN:
            return

    last_message_time[user_id] = now

    text = message.text or "📎 Медиа-сообщение"

    await bot.send_message(
        ADMIN_ID,
        f"📩 Новое сообщение:\n\n{text}"
    )

    await message.answer("✅ Сообщение доставлено")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
