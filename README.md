# Telegram AI Assistant 🤖

Этот проект — Telegram-бот с поддержкой GPT-4 и Whisper (голосовое распознавание).

## 🚀 Как развернуть (Render)

1. Заливаешь этот проект в GitHub
2. Идёшь на [https://render.com](https://render.com)
3. Создаёшь новый Web Service → подключаешь репозиторий
4. Настраиваешь:

**Start command:**
```
python bot.py
```

**Build command:**
```
pip install -r requirements.txt
```

**Environment:**
- `TELEGRAM_TOKEN=твой_токен`
- `OPENAI_API_KEY=твой_ключ`

## ✅ Функции

- Поддерживает текстовые сообщения → GPT
- Поддерживает голосовые → Whisper + GPT