import logging

import telebot
from telebot import types

from config import BOT_TOKEN
from openai_client import get_openai_response
from context_manager import ContextManager


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
context_manager = ContextManager()


@bot.message_handler(commands=["start"])
def cmd_start(message: types.Message) -> None:
    text = (
        "Привет! Я бот с GPT-5-mini. Напиши мне что-нибудь, и я отвечу.\n"
        "Используй /clear чтобы очистить контекст диалога."
    )
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["clear"])
def cmd_clear(message: types.Message) -> None:
    user_id = message.from_user.id
    context_manager.clear_context(user_id)
    bot.send_message(message.chat.id, "Контекст диалога очищен.")


@bot.message_handler(content_types=["text"])
def handle_message(message: types.Message) -> None:
    user_id = message.from_user.id
    user_text = message.text

    if not user_text:
        return

    if user_text.lower().strip() == "очистить контекст":
        context_manager.clear_context(user_id)
        bot.send_message(message.chat.id, "Контекст диалога очищен.")
        return

    bot.send_chat_action(message.chat.id, "typing")

    try:
        context = context_manager.get_context(user_id)
        messages = context + [{"role": "user", "content": user_text}]

        response_text = get_openai_response(messages)

        context_manager.update_context(user_id, user_text, response_text)

        bot.send_message(message.chat.id, response_text)
    except ValueError as e:
        error_message = str(e)
        logger.error(f"Ошибка при обработке сообщения: {error_message}")
        bot.send_message(message.chat.id, f"❌ {error_message}")
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}", exc_info=True)
        bot.send_message(
            message.chat.id,
            "❌ Произошла ошибка при обработке запроса. Попробуйте позже.",
        )


def main() -> None:
    logger.info("Бот запущен")
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка при работе бота: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
