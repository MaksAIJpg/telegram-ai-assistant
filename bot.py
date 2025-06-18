import os
import logging
import openai
import whisper
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# === Загрузка ключей ===
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# === Логирование ===
logging.basicConfig(level=logging.INFO)

# === Whisper Model ===
whisper_model = whisper.load_model("base")

# === Команда /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Я твой AI-ассистент. Напиши или отправь голосовое сообщение.")

# === Обработка текста ===
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response["choices"][0]["message"]["content"]
    await update.message.reply_text(reply)

# === Обработка голосовых сообщений ===
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.voice.file_id)
    await file.download_to_drive("voice.ogg")

    result = whisper_model.transcribe("voice.ogg")
    text = result["text"]

    await update.message.reply_text(f"🗣 Расшифровка: {text}")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}]
    )
    reply = response["choices"][0]["message"]["content"]
    await update.message.reply_text(f"💬 Ответ: {reply}")

# === Основной запуск ===
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
