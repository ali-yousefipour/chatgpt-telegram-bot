import openai
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
from dotenv import load_dotenv
from flask import Flask, request
import threading
import asyncio
from werkzeug.utils import url_quote
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

# تابع اصلی برای راه‌اندازی ربات تلگرام
async def telegram_main():
    # ساخت اپلیکیشن تلگرام
    application = Application.builder().token(BOT_TOKEN).build()

    # ثبت دستورات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # شروع پردازش پیام‌ها
    await application.run_polling()

# راه‌اندازی سرور Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Flask server is running!"

# اجرای Flask در یک thread جداگانه
def run_flask():
    app.run(host='0.0.0.0', port=5000)

# تابع اصلی برای اجرای Flask و ربات تلگرام هم‌زمان
async def main():
    # راه‌اندازی Flask در یک thread جداگانه
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # راه‌اندازی ربات تلگرام
    await telegram_main()

# اجرای اپلیکیشن با استفاده از asyncio
if __name__ == "__main__":
    asyncio.run(main())
