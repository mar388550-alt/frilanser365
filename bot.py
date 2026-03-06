import os
from flask import Flask
import threading
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ.get("BOT_TOKEN")
SECRET_SITE_LINK = os.environ.get("SECRET_SITE_LINK", "https://example.com")

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Бот готов к проверке!\n"
        "Нажмите кнопку, чтобы получить ссылку (демо).",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Получить ссылку", callback_data="get_link")]
        ])
    )

@dp.callback_query(lambda c: c.data == "get_link")
async def get_link(callback: types.CallbackQuery):
    await callback.message.answer(f"✅ Ваша ссылка: {SECRET_SITE_LINK}")
    await callback.answer()

@app.route('/')
def home():
    return "Bot is running"

def run_bot():
    asyncio.run(dp.start_polling(bot))

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
