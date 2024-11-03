import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api/auth/register"
HEADERS = {"Content-Type": "application/json"}


@pytest.fixture
def unique_email():
    """Генератор уникальных email для тестов"""
    import uuid
    return f"test-{uuid.uuid4()}@yandex.ru"


def test_create_unique_user(unique_email):
    """Тест создания уникального пользователя"""
    data = {
        "email": unique_email,
        "password": "password123",
        "name": "TestUser"
    }
    response = requests.post(BASE_URL, json=data, headers=HEADERS)

    # Проверяем успешность запроса
    assert response.status_code == 200
    assert response.json().get("success") is True


def test_create_existing_user():
    """Тест создания пользователя, который уже зарегистрирован"""
    data = {
        "email": "existinguser@yandex.ru",  # Убедитесь, что этот пользователь уже существует в системе
        "password": "password123",
        "name": "ExistingUser"
    }
    response = requests.post(BASE_URL, json=data, headers=HEADERS)

    # Проверяем, что при повторной регистрации приходит правильный ответ
    assert response.status_code == 403
    assert response.json().get("success") is False
    assert response.json().get("message") == "User already exists"


@pytest.mark.parametrize("missing_field, payload", [
    ("email", {"password": "password123", "name": "NoEmailUser"}),
    ("password", {"email": "test-no-password@yandex.ru", "name": "NoPasswordUser"}),
    ("name", {"email": "test-no-name@yandex.ru", "password": "password123"})
])
def test_create_user_with_missing_fields(missing_field, payload):
    """Тест создания пользователя без одного из обязательных полей"""
    response = requests.post(BASE_URL, json=payload, headers=HEADERS)

    # Проверяем, что запрос отклоняется с кодом 403
    assert response.status_code == 403
    assert response.json().get("success") is False
    assert "message" in response.json()


if __name__ == '__main__':
    pytest.main()