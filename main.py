import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import requests

TELEGRAM_TOKEN = '7252561996:AAG7XhwfAkfBGbVQ5OAWtZ6vkWPFOoxyVfU'
OPENAI_API_KEY = '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'

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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = await chatgpt_response(user_message)
    await update.message.reply_text(reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    PORT = int(os.environ.get('PORT', 8443))
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/"
    )
