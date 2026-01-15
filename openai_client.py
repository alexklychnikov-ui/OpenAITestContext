import logging
from openai import OpenAI, APIError, APIConnectionError, APITimeoutError
from config import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)

_client = None

def get_client():
    """Получить клиент OpenAI (ленивая инициализация)"""
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client

def get_openai_response(messages: list) -> str:
    """Получить ответ от OpenAI"""
    try:
        client = get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages
        )
        return response.choices[0].message.content
    except APIError as e:
        error_code = getattr(e, 'code', None)
        if error_code == 'unsupported_country_region_territory':
            logger.error(f"OpenAI API недоступен в вашем регионе: {e}")
            raise ValueError("OpenAI API недоступен в вашем регионе. Используйте VPN или прокси.")
        logger.error(f"Ошибка API OpenAI: {e}")
        raise
    except (APIConnectionError, APITimeoutError) as e:
        logger.error(f"Ошибка подключения к OpenAI: {e}")
        raise ValueError("Ошибка подключения к OpenAI API. Проверьте интернет-соединение.")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при обращении к OpenAI: {e}")
        raise
