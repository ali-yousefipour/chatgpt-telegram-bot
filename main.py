import os
import openai
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, CommandHandler, filters
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از .env (در صورت نیاز)
load_dotenv()

# گرفتن توکن‌ها از متغیر محیطی
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# تنظیم کلید API
openai.api_key = OPENAI_API_KEY

# پاسخ اولیه هنگام شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات ChatGPT هستم. هر سوالی داشتی بپرس.")

# هندل پیام‌های متنی
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("متاسفم، مشکلی پیش اومد.")
        print(f"خطا: {e}")

# اجرای اصلی ربات
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("ربات در حال اجراست...")
    app.run_polling()

if __name__ == "__main__":
    main()
