import openai
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
from dotenv import load_dotenv
import asyncio
from flask import Flask
from threading import Thread

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# تنظیمات مربوط به توکن تلگرام و کلید OpenAI
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# تنظیمات لاگ‌گذاری
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

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

# تابع اصلی برای راه‌اندازی ربات
async def telegram_main():
    # ساخت اپلیکیشن تلگرام
    application = Application.builder().token(BOT_TOKEN).build()

    # ثبت دستورات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # شروع پردازش پیام‌ها
    await application.run_polling()

# راه‌اندازی Flask به صورت جداگانه در یک نخ جدید
def run_flask():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "Flask is running!"

    app.run(host='0.0.0.0', port=5000)

# اجرای Flask و ربات تلگرام به صورت موازی
if __name__ == "__main__":
    # ایجاد و شروع یک نخ جداگانه برای اجرای Flask
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # اجرای Telegram Bot با استفاده از asyncio
    asyncio.create_task(telegram_main())
    asyncio.get_event_loop().run_forever()
