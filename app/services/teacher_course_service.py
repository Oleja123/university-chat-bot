import logging

import requests

from app.exceptions.non_authorized_error import NonAuthorizedError
from config import Config
from app.models.notification import Notifification
from app.models.teacher_course import TeacherCourse
from app.services.from_json_collection import from_json_collection


logger = logging.getLogger(__name__)


def get_all_paginated(user_id: int, token: str, page: int = None) -> list[Notifification]:
    if page is None:
        page = 1
    query = Config.API_BASE_URL + f"/users/{user_id}/courses?page={page}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(query, headers=headers)
    try:
        response.raise_for_status()
        list = from_json_collection(response.json(), TeacherCourse)
        logger.info(f"Полученные курсы пользователя {list['items']}")
        return list
    except requests.HTTPError as e:
        logger.error(e)
        if response.status_code == 401:
            raise NonAuthorizedError("Ошибка авторизации")
        if response.status_code == 404:
            raise Exception("Ресурс не найден")
        raise Exception(f"Ошибка api")
    except Exception as e:
        logger.error(e)
        raise Exception('Ошибка при запросе к API')


def get_by_ids(user_id: int, course_id: int, token: str):
    query = Config.API_BASE_URL + f"/users/{user_id}/courses/{course_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(query, headers=headers)
    try:
        response.raise_for_status()
        teaher_course = TeacherCourse.from_dict(response.json())
        logger.info(f"Полученный курс пользователя {teaher_course}")
        return teaher_course
    except requests.HTTPError as e:
        logger.error(e)
        if response.status_code == 401:
            raise NonAuthorizedError("Ошибка авторизации")
        if response.status_code == 404:
            raise Exception("Ресурс не найден")
        raise Exception(f"Ошибка api")
    except Exception as e:
        logger.error(e)
        raise Exception('Ошибка при запросе к API')


def download_teacher_course(user_id: int, course_id: int, token: str):
    query = Config.API_BASE_URL + \
        f"/users/{user_id}/courses/{course_id}/download"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(query, headers=headers)
    try:
        response.raise_for_status()
        logger.info('response.content')
        with open("temp.pdf", "wb") as f:
            f.write(response.content)
        logger.info(
            f"Получен сертификат пользователя {user_id} по курсу {course_id}")
        return f
    except requests.HTTPError as e:
        if response.status_code == 401:
            raise NonAuthorizedError("Ошибка авторизации")
        if response.status_code == 404:
            raise Exception("Ресурс не найден")
        raise Exception(f"Ошибка api")
    except Exception as e:
        logger.error(e)
        raise Exception('Ошибка при запросе к API')
