from uuid import uuid4

import pytest
import requests

from config import BASE_URL, INGREDIENTS_ENDPOINT, REGISTER_ENDPOINT


@pytest.fixture
def api_session():
    with requests.Session() as session:
        yield session


@pytest.fixture
def user_data():
    return {
        "email": f"autotest_{uuid4().hex[:12]}@yandex.ru",
        "password": "TestPassword123!",
        "name": "API Test User",
    }


@pytest.fixture
def registered_user(api_session, user_data):
    response = api_session.post(
        f"{BASE_URL}{REGISTER_ENDPOINT}",
        json=user_data,
    )

    access_token = response.json()["accessToken"]

    yield {
        "data": user_data,
        "access_token": access_token,
    }

    api_session.delete(
        f"{BASE_URL}/auth/user",
        headers={"Authorization": access_token},
    )


@pytest.fixture
def ingredient_ids(api_session):
    response = api_session.get(
        f"{BASE_URL}{INGREDIENTS_ENDPOINT}"
    )

    return [ingredient["_id"] for ingredient in response.json()["data"]]

@pytest.fixture
def tokens_to_delete(api_session):
    tokens = []

    yield tokens

    for token in tokens:
        api_session.delete(
            f"{BASE_URL}/auth/user",
            headers={"Authorization": token},
        )