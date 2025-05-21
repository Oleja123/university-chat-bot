import requests

from config import Config


def login(username, password):
    query = Config.API_BASE_URL + f"/tokens"
    response = requests.post(query, auth=(username,password))
    try:
        response.raise_for_status()
        return response.json()['token']
    except requests.HTTPError as e:
        if response.status_code == 400:
            raise Exception("Пользователь не найден")
        elif response.status_code == 401:
            raise Exception("Неверный пароль")
        elif response.status_code == 403:
            raise Exception("Пользователь заблокирован")
        else:
            raise Exception(f"Ошибка api")
    except Exception as e:
        raise Exception('Неизвестная ошибка')