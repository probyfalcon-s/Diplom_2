import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api/auth/user"
HEADERS = {"Content-Type": "application/json"}


@pytest.fixture
def access_token():
    """Фикстура для получения access token через авторизацию"""
    login_url = "https://stellarburgers.nomoreparties.site/api/auth/login"
    data = {
        "email": "existinguser@yandex.ru",  # Существующий пользователь
        "password": "password123"
    }
    response = requests.post(login_url, json=data, headers=HEADERS)
    token = response.json().get("accessToken")
    return token


@pytest.fixture
def user_data():
    """Фикстура с данными пользователя для обновления"""
    return {
        "email": "newemail@yandex.ru",
        "name": "NewUserName"
    }


@pytest.fixture
def existing_email_data():
    """Фикстура с данными, где email уже существует"""
    return {
        "email": "existinguser@yandex.ru",
        "name": "DuplicateName"
    }


def test_update_user_with_authorization(access_token, user_data):
    """Тест обновления данных пользователя с авторизацией"""
    headers_with_auth = {
        "Content-Type": "application/json",
        "Authorization": access_token  # Добавляем access token
    }
    response = requests.patch(BASE_URL, json=user_data, headers=headers_with_auth)

    # Проверяем успешность запроса
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("success") is True
    assert response_data.get("user")["email"] == user_data["email"]
    assert response_data.get("user")["name"] == user_data["name"]


def test_update_user_without_authorization(user_data):
    """Тест попытки обновления данных без авторизации"""
    response = requests.patch(BASE_URL, json=user_data, headers=HEADERS)

    # Проверяем, что запрос отклонён с кодом 401
    assert response.status_code == 401
    response_data = response.json()
    assert response_data.get("success") is False
    assert response_data.get("message") == "You should be authorised"


def test_update_user_with_existing_email(access_token, existing_email_data):
    """Тест обновления с использованием email, который уже зарегистрирован"""
    headers_with_auth = {
        "Content-Type": "application/json",
        "Authorization": access_token
    }
    response = requests.patch(BASE_URL, json=existing_email_data, headers=headers_with_auth)

    # Проверяем, что запрос отклонён с кодом 403
    assert response.status_code == 403
    response_data = response.json()
    assert response_data.get("success") is False
    assert response_data.get("message") == "User with such email already exists"


if __name__ == '__main__':
    pytest.main()