import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api/orders"
HEADERS = {"Content-Type": "application/json"}


@pytest.fixture
def access_token():
    """Фикстура для получения access token через авторизацию"""
    login_url = "https://stellarburgers.nomoreparties.site/api/auth/login"
    data = {
        "email": "existinguser@yandex.ru",  # Замените на существующего пользователя
        "password": "password123"
    }
    response = requests.post(login_url, json=data, headers=HEADERS)
    token = response.json().get("accessToken")
    return token


def test_get_orders_authorized_user(access_token):
    """Тест получения заказов для авторизованного пользователя"""
    headers_with_auth = {
        "Content-Type": "application/json",
        "Authorization": access_token
    }
    response = requests.get(BASE_URL, headers=headers_with_auth)

    # Проверяем успешность запроса
    assert response.status_code == 200
    response_data = response.json()

    # Проверяем, что ответ успешен и есть поле 'orders'
    assert response_data.get("success") is True
    assert "orders" in response_data
    assert len(response_data["orders"]) <= 50  # Максимум 50 заказов
    assert "total" in response_data
    assert "totalToday" in response_data


def test_get_orders_unauthorized_user():
    """Тест получения заказов для неавторизованного пользователя (ожидается ошибка 401)"""
    response = requests.get(BASE_URL, headers=HEADERS)

    # Проверяем, что вернулась ошибка 401 Unauthorized
    assert response.status_code == 401
    response_data = response.json()

    assert response_data.get("success") is False
    assert response_data.get("message") == "You should be authorised"


if __name__ == '__main__':
    pytest.main()