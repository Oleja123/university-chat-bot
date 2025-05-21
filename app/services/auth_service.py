import requests

from config import Config


def login(username, password):
    query = Config.API_BASE_URL + f"/tokens"
    response = requests(query, auth=(username,password))
    try:
        response.raise_for_status()
        return response.json()['token']
    except requests.HTTPError as e:
        if response.status_code == 400:
            print("Пользователь не найден")
        elif response.status_code == 401:
            print("Неверный пароль")
        elif response.status_code == 403:
            print("Пользователь заблокирован")
        else:
            print(f"Ошибка api")