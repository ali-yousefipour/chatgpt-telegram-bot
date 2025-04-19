import os
import logging
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import asyncio

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# تنظیمات لاگ‌گذاری
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# بارگذاری توکن تلگرام و API Key از فایل .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# تنظیمات OpenAI API
openai.api_key = OPENAI_API_KEY

# تابع برای ارسال پیام به OpenAI و دریافت جواب
async def get_openai_response(message: str) -> str:
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # مدل GPT-3
            prompt=message,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logger.error(f"Error with OpenAI API: {e}")
        return "An error occurred while fetching the response."

# تابع شروع ربات
async def start(update: Update, context):
    await update.message.reply_text("سلام! من ربات ChatGPT هستم. چطور می‌توانم به شما کمک کنم؟")

# تابع برای پردازش پیام‌ها در تلگرام
async def handle_message(update: Update, context):
    user_message = update.message.text
    logger.info(f"Received message: {user_message}")
    
    # دریافت پاسخ از OpenAI
    response = await get_openai_response(user_message)
    
    # ارسال پاسخ به کاربر
    await update.message.reply_text(response)

# تابع اصلی برای راه‌اندازی ربات تلگرام
async def telegram_main():
    # ساخت اپلیکیشن تلگرام
    application = Application.builder().token(BOT_TOKEN).build()

    # ثبت دستورات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # شروع پردازش پیام‌ها
    await application.run_polling()

# اجرای برنامه
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(telegram_main())
