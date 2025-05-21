import requests

from app.exceptions.non_authorized_error import NonAuthorizedError
from config import Config
from models.notification import Notifification
from services.from_json_collection import from_json_collection
from run import logger


def get_all_paginated(user_id: int, token: str, page: int = None) -> list[Notifification]:
    if page is None:
        page = 1
    query = Config.API_BASE_URL + f"/users/{user_id}/notifications?page={page}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(query, headers=headers)
    try:
        response.raise_for_status()
        list = from_json_collection(response.json())
        logger.info(f"Полученные уведомления пользователя {list['items']}")
        return list
    except requests.HTTPError as e:
        if response.status_code == 401:
            raise NonAuthorizedError("Ошибка авторизации")
        if response.status_code == 404:
            raise Exception("Ресурс не найден")
        raise Exception(f"Ошибка api")
    except Exception as e:
        logger.error(e)
        raise Exception('Ошибка при запросе к API')


def get_by_id(id: int, token: str):
    query = Config.API_BASE_URL + f"/notifications/{id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(query, headers=headers)
    try:
        response.raise_for_status()
        notifification = Notifification.from_dict(response.json())
        logger.info(f"Полученное уведомление пользователя {notifification}")
        return notifification
    except requests.HTTPError as e:
        if response.status_code == 401:
            raise NonAuthorizedError("Ошибка авторизации")
        if response.status_code == 404:
            raise Exception("Ресурс не найден")
        raise Exception(f"Ошибка api")
    except Exception as e:
        logger.error(e)
        raise Exception('Ошибка при запросе к API')


def read(id: int, token: str):
    query = Config.API_BASE_URL + f"/notifications/{id}/read"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(query, headers=headers)
    try:
        response.raise_for_status()
        notifification = Notifification.from_dict(response.json())
        logger.info(f"Прочитано уведомление пользователя {notifification}")
        return notifification
    except requests.HTTPError as e:
        if response.status_code == 401:
            raise NonAuthorizedError("Ошибка авторизации")
        if response.status_code == 404:
            raise Exception("Ресурс не найден")
        raise Exception(f"Ошибка api")
    except Exception as e:
        logger.error(e)
        raise Exception('Ошибка при запросе к API')


def delete_notification(id: int, token: str):
    query = Config.API_BASE_URL + f"/notifications/{id}/delete"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(query, headers=headers)
    try:
        response.raise_for_status()
        logger.info(f"Уведомление пользователя {id} удалено")
    except requests.HTTPError as e:
        if response.status_code == 401:
            raise NonAuthorizedError("Ошибка авторизации")
        if response.status_code == 404:
            raise Exception("Ресурс не найден")
        raise Exception(f"Ошибка api")
    except Exception as e:
        logger.error(e)
        raise Exception('Ошибка при запросе к API')
