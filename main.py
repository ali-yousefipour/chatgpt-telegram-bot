import openai
import logging
from flask import Flask, request
from flask_socketio import SocketIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
from dotenv import load_dotenv
import asyncio

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# تنظیمات مربوط به توکن تلگرام و کلید OpenAI
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# تنظیمات لاگ‌گذاری
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# تنظیمات Flask
app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# تابع برای ارسال پیام به OpenAI و دریافت جواب
async def get_openai_response(message: str):
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logger.error(f"Error with OpenAI API: {e}")
        return "An error occurred while fetching the response."

# تابع برای پردازش پیام‌ها در تلگرام
async def handle_message(update: Update, context):
    user_message = update.message.text
    logger.info(f"Received message: {user_message}")
    
    # دریافت پاسخ از OpenAI
    response = await get_openai_response(user_message)
    
    # ارسال پاسخ به کاربر
    await update.message.reply_text(response)

# دستور شروع ربات
async def start(update: Update, context):
    await update.message.reply_text("Hello! I'm your friendly ChatGPT bot. How can I assist you today?")

# تابع اصلی برای راه‌اندازی ربات تلگرام
async def telegram_main():
    # ساخت اپلیکیشن تلگرام
    application = Application.builder().token(BOT_TOKEN).build()

    # ثبت دستورات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # شروع پردازش پیام‌ها
    await application.run_polling()

# تابع راه‌اندازی Flask و ربات تلگرام به صورت همزمان
async def main():
    # اجرای ربات تلگرام به صورت async
    loop = asyncio.get_event_loop()

    # اجرای ربات تلگرام به صورت همزمان
    loop.create_task(telegram_main())

    # راه‌اندازی سرور Flask
    socketio.run(app, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    # استفاده از asyncio.run برای اجرای حلقه رویداد
    asyncio.run(main())
