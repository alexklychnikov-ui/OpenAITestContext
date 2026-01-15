# Telegram бот с OpenAI GPT-5-mini

Telegram-бот на Python с использованием aiogram и OpenAI API.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте файл `.env` на основе `.env.example`:
```
BOT_TOKEN=ваш_токен_бота
OPENAI_API_KEY=ваш_openai_ключ
```

3. Запустите бота:
```bash
python bot.py
```

## Команды

- `/start` - приветствие
- `/clear` - очистить контекст диалога
- "очистить контекст" - также очищает контекст
