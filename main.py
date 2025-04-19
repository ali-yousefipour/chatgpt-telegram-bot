import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# توکن ربات تلگرام شما
TELEGRAM_TOKEN = '7252561996:AAG7XhwfAkfBGbVQ5OAWtZ6vkWPFOoxyVfU'
# کلید API چت‌جی‌پی‌تی شما
OPENAI_API_KEY = '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'

logging.basicConfig(level=logging.INFO)

# تابع ارسال درخواست به ChatGPT
async def chatgpt_response(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    try:
        return result['choices'][0]['message']['content'].strip()
    except:
        return "متاسفم، مشکلی پیش اومد."

# تابع دریافت پیام از تلگرام و ارسال پاسخ
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = await chatgpt_response(user_message)
    await update.message.reply_text(reply)

# تنظیمات و اجرای ربات
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
