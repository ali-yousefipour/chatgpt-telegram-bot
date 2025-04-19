import os
import logging
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from flask import Flask, request

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# تنظیم توکن ربات تلگرام و کلید API OpenAI
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# تنظیمات OpenAI
openai.api_key = OPENAI_API_KEY

# ساخت اپلیکیشن Flask برای اتصال به پورت
app = Flask(__name__)

# تنظیمات Telegram
application = Application.builder().token(BOT_TOKEN).build()

# تعریف دستور /start برای ربات تلگرام
async def start(update: Update, context):
    await update.message.reply_text("سلام! من آماده هستم تا به سوالات شما پاسخ بدهم.")

# تعریف دستوری برای دریافت پیام و ارسال پاسخ از OpenAI
async def handle_message(update: Update, context):
    user_message = update.message.text
    try:
        # ارسال پیام به OpenAI برای دریافت پاسخ
        response = openai.Completion.create(
            model="text-davinci-003",  # مدل OpenAI
            prompt=user_message,
            max_tokens=150
        )
        answer = response.choices[0].text.strip()
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text("متاسفانه مشکلی پیش آمد.")

# اضافه کردن هندلرها به ربات
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# راه‌اندازی سرور Flask برای پورت و دریافت درخواست‌ها
@app.route("/")
def index():
    return "ربات تلگرام در حال اجراست!"

# تابع اصلی برای شروع ربات تلگرام
if __name__ == "__main__":
    # شروع وب سرویس Flask و ربات تلگرام
    import threading
    threading.Thread(target=lambda: application.run_polling()).start()
    app.run(host="0.0.0.0", port=8000)
