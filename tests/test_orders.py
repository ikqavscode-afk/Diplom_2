import allure

from config import BASE_URL, ORDERS_ENDPOINT


class TestOrders:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(
        self,
        api_session,
        registered_user,
        ingredient_ids,
    ):
        headers = {
            "Authorization": registered_user["access_token"],
        }
        order_data = {
            "ingredients": ingredient_ids[:2],
        }

        with allure.step("Отправить запрос на создание заказа"):
            response = api_session.post(
                f"{BASE_URL}{ORDERS_ENDPOINT}",
                json=order_data,
                headers=headers,
            )

        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == 200, response.text

            body = response.json()
            assert body["success"] is True
            assert body["order"]["number"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, api_session, ingredient_ids):
        order_data = {
            "ingredients": ingredient_ids[:2],
        }

        with allure.step("Отправить запрос без токена авторизации"):
            response = api_session.post(
                f"{BASE_URL}{ORDERS_ENDPOINT}",
                json=order_data,
            )

        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == 200, response.text

            body = response.json()
            assert body["success"] is True
            assert body["order"]["number"]

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(
        self,
        api_session,
        registered_user,
    ):
        headers = {
            "Authorization": registered_user["access_token"],
        }

        with allure.step("Отправить авторизованный запрос без ингредиентов"):
            response = api_session.post(
                f"{BASE_URL}{ORDERS_ENDPOINT}",
                json={"ingredients": []},
                headers=headers,
            )

        with allure.step("Проверить ошибку отсутствующих ингредиентов"):
            assert response.status_code == 400, response.text
            assert response.json()["success"] is False
            assert (
                response.json()["message"]
                == "Ingredient ids must be provided"
            )

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash(
        self,
        api_session,
        registered_user,
    ):
        headers = {
            "Authorization": registered_user["access_token"],
        }
        order_data = {
            "ingredients": ["invalid-ingredient-hash"],
        }

        with allure.step("Отправить заказ с неверным ID ингредиента"):
            response = api_session.post(
                f"{BASE_URL}{ORDERS_ENDPOINT}",
                json=order_data,
                headers=headers,
            )

        with allure.step("Проверить ошибку неверного ID ингредиента"):
            assert response.status_code == 500, response.text
