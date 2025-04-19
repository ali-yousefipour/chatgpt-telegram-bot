import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# گرفتن توکن‌ها از متغیر محیطی
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# تنظیم لاگ‌گیری برای دیباگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# تابع دریافت پاسخ از ChatGPT
def chatgpt_response(message_text):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message_text}]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    print("RAW RESPONSE:", response.text)  # برای دیباگ

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "متاسفم، مشکلی پیش اومد."

# هندلر پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = chatgpt_response(user_message)
    await update.message.reply_text(reply)

# اجرای بات
if __name__ == '__main__':
    if not BOT_TOKEN or not OPENAI_API_KEY:
        raise RuntimeError("توکن‌ها به درستی تنظیم نشده‌اند.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
