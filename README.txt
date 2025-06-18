=== УСТАНОВКА НА RENDER ===

1. Перейди на https://render.com
2. Создай новый Web Service
3. Загрузи этот архив
4. Добавь файл `.env` со значениями из `.env.example`
5. Укажи start command: python bot.py
6. Убедись, что тип — **Background Worker**
7. Нажми Deploy

Бот начнёт слушать голосовые и расшифровывать их.

Важно:
- Render не поддерживает ffmpeg по умолчанию. Файл .ogg должен быть обработан через Whisper напрямую (в обход ffmpeg).
- Убедись, что ключи TELEGRAM и OpenAI рабочие.
