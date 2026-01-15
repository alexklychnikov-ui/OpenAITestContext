# Telegram‑бот с OpenAI (GPT‑5-mini)

Telegram‑бот на Python с использованием **pyTelegramBotAPI** и **OpenAI Chat Completions API**.  
Бот хранит контекст диалога в памяти процесса и отправляет его в OpenAI для получения ответа.

## Требования

- Python 3.11+ (у тебя сейчас 3.13)
- Аккаунт OpenAI и API‑ключ
- Токен Telegram‑бота

## Установка и запуск

Рекомендуемый вариант — через `venv` (у тебя уже настроен).

1. **Клонировать репозиторий**:
   ```bash
   git clone https://github.com/alexklychnikov-ui/OpenAITestContext.git
   cd OpenAITestContext
   ```

2. **Создать и активировать виртуальное окружение (если ещё нет)**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Установить зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Создать файл `.env`** рядом с `config.py`:
   ```env
   BOT_TOKEN=ваш_токен_бота
   OPENAI_API_KEY=ваш_openai_ключ
   ```

5. **Запустить бота**:
   ```bash
   python bot.py
   ```

## Поведение и команды

- `/start` — приветствие и краткая инструкция
- `/clear` — очистить контекст диалога
- текст `"очистить контекст"` — тоже очищает контекст

Все остальные текстовые сообщения:
- добавляются в контекст пользователя
- отправляются в OpenAI (`openai_client.get_openai_response`)
- ответ сохраняется в контекст и отправляется обратно в чат

## Важные замечания

- В некоторых регионах OpenAI API может быть **недоступен** — в этом случае бот вернёт понятное сообщение  
  (`unsupported_country_region_territory`, см. `openai_client.py`).
- Для обхода ограничений возможен вариант с VPN/прокси на уровне сервера.
