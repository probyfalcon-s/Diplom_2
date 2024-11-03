import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api/auth/login"
HEADERS = {"Content-Type": "application/json"}

@pytest.fixture
def valid_user():
    """Фикстура с данными существующего пользователя"""
    return {
        "email": "existinguser@yandex.ru",  # Убедитесь, что этот пользователь зарегистрирован
        "password": "password123"
    }

@pytest.fixture
def invalid_user():
    """Фикстура с неверными данными для логина"""
    return {
        "email": "wrongemail@yandex.ru",
        "password": "wrongpassword"
    }

def test_login_existing_user(valid_user):
    """Тест логина под существующим пользователем"""
    response = requests.post(BASE_URL, json=valid_user, headers=HEADERS)

    # Проверяем успешность авторизации
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("success") is True
    assert "accessToken" in response_data
    assert "refreshToken" in response_data
    assert "user" in response_data
    assert response_data["user"]["email"] == valid_user["email"]

def test_login_invalid_user(invalid_user):
    """Тест логина с неверным email или паролем"""
    response = requests.post(BASE_URL, json=invalid_user, headers=HEADERS)

    # Проверяем, что запрос отклонён с кодом 401
    assert response.status_code == 401
    response_data = response.json()
    assert response_data.get("success") is False
    assert response_data.get("message") == "email or password are incorrect"


if __name__ == '__main__':
    pytest.main()