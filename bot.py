import os
import logging
import openai
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)
import aiohttp
import tempfile

# Логирование
logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Установка ключа OpenAI
openai.api_key = OPENAI_API_KEY

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Я твой AI-ассистент. Напиши мне сообщение или пришли голосовое.")

# Текстовое сообщение → GPT
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    reply = response.choices[0].message["content"]
    await update.message.reply_text(reply)

# Голосовое сообщение → Whisper → GPT
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.voice.file_id)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as f:
        await file.download_to_drive(f.name)
        f_path = f.name

    audio_file = open(f_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    text = transcript["text"]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}],
        temperature=0.7,
    )
    reply = response.choices[0].message["content"]
    await update.message.reply_text(f"🗣 Расшифровка: {text}")
    await update.message.reply_text(f"💬 Ответ: {reply}")

# Запуск бота
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
