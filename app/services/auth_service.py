import logging

import requests

from config import Config

logger = logging.getLogger(__name__)

def login(username, password):
    logger.info('Я ТУТ')
    query = Config.API_BASE_URL + f"/tokens"
    response = requests.post(query, auth=(username,password), verify=False)
    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        if response.status_code == 400:
            raise ValueError("Пользователь не найден")
        elif response.status_code == 401:
            raise ValueError("Неверный пароль")
        elif response.status_code == 403:
            raise ValueError("Пользователь заблокирован")
        else:
            raise Exception(f"Ошибка api")
    except Exception as e:
        logger.error(e)
        raise Exception('Неизвестная ошибка')