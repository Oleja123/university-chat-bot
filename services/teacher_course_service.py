import requests

from config import Config
from models.notification import Notifification
from models.teacher_course import TeacherCourse
from services.from_json_collection import from_json_collection
from main import logger


def get_all_paginated(user_id: int, page: int = None) -> list[Notifification]:
    if page is None:
        page = 1
    query = Config.API_BASE_URL + f"/users/{user_id}/courses?page={page}"
    response = requests.get(query)
    try:
        response.raise_for_status()
        list = from_json_collection(response.json())
        logger.info(f"Полученные курсы пользователя {list['items']}")
        return list
    except Exception as e:
        logger.error(e)
        raise Exception('Ошибка при запросе к API')


def get_by_ids(user_id, course_id):
    query = Config.API_BASE_URL + f"/users/{user_id}/courses/{course_id}"
    response = requests.get(query)
    try:
        response.raise_for_status()
        teaher_course = TeacherCourse.from_dict(response.json())
        logger.info(f"Полученный курс пользователя {teaher_course}")
        return teaher_course
    except Exception as e:
        logger.error(e)
        raise Exception('Ошибка при запросе к API')


def download_teacher_course(user_id, course_id):
    query = Config.API_BASE_URL + f"/users/{user_id}/courses/{course_id}/download"
    response = requests.get(query)
    try:
        response.raise_for_status()
        with open("temp.pdf", "wb") as f:
            f.write(response.content)
        logger.info(f"Получен сертификат пользователя {user_id} по курсу {course_id}")
        return f
    except Exception as e:
        logger.error(e)
        raise Exception('Ошибка при запросе к API')
