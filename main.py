import logging
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
from dotenv import load_dotenv

load_dotenv()  # بارگذاری متغیرهای محیطی از فایل .env

openai.api_key = os.getenv('OPENAI_API_KEY')
bot_token = os.getenv('BOT_TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text("سلام! من ربات ChatGPT هستم. چطور می‌توانم به شما کمک کنم؟")

async def chatgpt(update: Update, context):
    prompt = update.message.text  # پیام دریافتی از کاربر
    response = openai.Completion.create(
        engine="text-davinci-003",  # مدل ChatGPT
        prompt=prompt,
        max_tokens=150
    )
    answer = response.choices[0].text.strip()  # گرفتن جواب از API OpenAI
    await update.message.reply_text(answer)  # ارسال جواب به کاربر

async def main():
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt))

    # به جای asyncio.run از اینجا شروع کنید
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
