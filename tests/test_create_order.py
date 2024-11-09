import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api/orders"
HEADERS = {"Content-Type": "application/json"}

@pytest.fixture
def access_token():
    login_url = "https://stellarburgers.nomoreparties.site/api/auth/login"
    data = {
        "email": "alexeysokolov13987@yandex.ru",  # Замените на существующего пользователя
        "password": "dBAn]C"
    }
    response = requests.post(login_url, json=data, headers=HEADERS)
    token = response.json().get("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2Yzg1YmU0OWVkMjgwMDAxYjQ5ZDk3ZSIsImlhdCI6MTczMTE4MTg5NSwiZXhwIjoxNzMxMTgzMDk1fQ.cVHGHLbt9G1qub4WKJZrLs1Z2TtbsJHnfuSTe_vgAko")
    return token

@pytest.fixture
def valid_ingredients():
    return ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]

@pytest.fixture
def invalid_ingredients():
    return ["invalid_hash"]

def test_create_order_with_authorization(access_token, valid_ingredients):
    headers_with_auth = {
        "Content-Type": "application/json",
        "Authorization": Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2Yzg1YmU0OWVkMjgwMDAxYjQ5ZDk3ZSIsImlhdCI6MTczMTE4MTg5NSwiZXhwIjoxNzMxMTgzMDk1fQ.cVHGHLbt9G1qub4WKJZrLs1Z2TtbsJHnfuSTe_vgAko
    }
    order_data = {
        "ingredients": valid_ingredients
    }
    response = requests.post(BASE_URL, json=order_data, headers=headers_with_auth)

    # Проверяем успешность запроса
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("success") is True
    assert "order" in response_data
    assert "number" in response_data["order"]

def test_create_order_without_authorization(valid_ingredients):
    order_data = {
        "ingredients": valid_ingredients
    }
    response = requests.post(BASE_URL, json=order_data, headers=HEADERS)

    # Проверяем успешность запроса (запрос должен проходить без авторизации)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("success") is True
    assert "order" in response_data
    assert "number" in response_data["order"]

def test_create_order_without_ingredients(access_token):
    headers_with_auth = {
        "Content-Type": "application/json",
        "Authorization": Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2Yzg1YmU0OWVkMjgwMDAxYjQ5ZDk3ZSIsImlhdCI6MTczMTE4MTg5NSwiZXhwIjoxNzMxMTgzMDk1fQ.cVHGHLbt9G1qub4WKJZrLs1Z2TtbsJHnfuSTe_vgAko
    }
    order_data = {
        "ingredients": []
    }
    response = requests.post(BASE_URL, json=order_data, headers=headers_with_auth)

    # Проверяем, что вернулась ошибка 400
    assert response.status_code == 400
    response_data = response.json()
    assert response_data.get("success") is False
    assert response_data.get("message") == "Ingredient ids must be provided"

def test_create_order_with_invalid_ingredients(access_token, invalid_ingredients):
    headers_with_auth = {
        "Content-Type": "application/json",
        "Authorization": Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2Yzg1YmU0OWVkMjgwMDAxYjQ5ZDk3ZSIsImlhdCI6MTczMTE4MTg5NSwiZXhwIjoxNzMxMTgzMDk1fQ.cVHGHLbt9G1qub4WKJZrLs1Z2TtbsJHnfuSTe_vgAko
    }
    order_data = {
        "ingredients": invalid_ingredients
    }
    response = requests.post(BASE_URL, json=order_data, headers=headers_with_auth)

    # Проверяем, что вернулась ошибка 500
    assert response.status_code == 500
    response_data = response.json()
    assert response_data.get("success") is False or response_data.get("message") == "Internal Server Error"

if __name__ == '__main__':
    pytest.main()