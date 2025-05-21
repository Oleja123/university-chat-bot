import requests

from config import Config
from models.notification import Notifification
from services.from_json_collection import from_json_collection
from run import logger


def get_all_paginated(user_id: int, page: int = None) -> list[Notifification]:
    if page is None:
        page = 1
    query = Config.API_BASE_URL + f"/users/{user_id}/notifications?page={page}"
    response = requests.get(query)
    try:
        response.raise_for_status()
        list = from_json_collection(response.json())
        logger.info(f"Полученные уведомления пользователя {list['items']}")
        return list
    except Exception as e:
        logger.error(e)
        raise Exception('Ошибка при запросе к API')


def get_by_id(id):
    query = Config.API_BASE_URL + f"/notifications/{id}"
    response = requests.get(query)
    try:
        response.raise_for_status()
        notifification = Notifification.from_dict(response.json())
        logger.info(f"Полученное уведомление пользователя {notifification}")
        return notifification
    except Exception as e:
        logger.error(e)
        raise Exception('Ошибка при запросе к API')


def read(id):
    query = Config.API_BASE_URL + f"/notifications/{id}/read"
    response = requests.put(query)
    try:
        response.raise_for_status()
        notifification = Notifification.from_dict(response.json())
        logger.info(f"Прочитано уведомление пользователя {notifification}")
        return notifification
    except Exception as e:
        logger.error(e)
        raise Exception('Ошибка при запросе к API')


def delete_notification(id):
    query = Config.API_BASE_URL + f"/notifications/{id}/delete"
    response = requests.delete(query)
    try:
        response.raise_for_status()
        logger.info(f"Уведомление пользователя {id} удалено")
    except Exception as e:
        logger.error(e)
        raise Exception('Ошибка при запросе к API')
