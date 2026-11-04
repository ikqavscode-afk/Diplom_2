import allure

from config import BASE_URL, LOGIN_ENDPOINT, REGISTER_ENDPOINT


class TestUserRegistration:
    @allure.title("Регистрация нового пользователя")
    def test_register_new_user(self, api_session, user_data, tokens_to_delete):
        with allure.step("Отправить данные нового пользователя"):
            response = api_session.post(
                f"{BASE_URL}{REGISTER_ENDPOINT}",
                json=user_data,
            )

        body = response.json()
        tokens_to_delete.append(body["accessToken"])

        with allure.step("Проверить успешный ответ и данные пользователя"):
            assert response.status_code == 200, response.text
            assert body["success"] is True
            assert body["user"]["email"] == user_data["email"]
            assert body["user"]["name"] == user_data["name"]
            assert body["accessToken"].startswith("Bearer ")
            assert body["refreshToken"]

    @allure.title("Повторная регистрация существующего пользователя")
    def test_register_existing_user(self, api_session, registered_user):
        with allure.step(
            "Повторно отправить данные зарегистрированного пользователя"
        ):
            response = api_session.post(
                f"{BASE_URL}{REGISTER_ENDPOINT}",
                json=registered_user["data"],
            )

        with allure.step("Проверить отказ в повторной регистрации"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == "User already exists"

    @allure.title("Регистрация без обязательного поля")
    def test_register_without_required_field(self, api_session, user_data):
        incomplete_user_data = {
            "email": user_data["email"],
            "password": user_data["password"],
        }

        with allure.step("Отправить данные без имени"):
            response = api_session.post(
                f"{BASE_URL}{REGISTER_ENDPOINT}",
                json=incomplete_user_data,
            )

        with allure.step("Проверить отказ из-за отсутствующего поля"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert (
                response.json()["message"]
                == "Email, password and name are required fields"
            )


class TestUserLogin:
    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user(self, api_session, registered_user):
        with allure.step("Войти с данными зарегистрированного пользователя"):
            response = api_session.post(
                f"{BASE_URL}{LOGIN_ENDPOINT}",
                json=registered_user["data"],
            )

        with allure.step("Проверить успешную авторизацию"):
            assert response.status_code == 200, response.text

            body = response.json()
            assert body["success"] is True
            assert body["user"]["email"] == registered_user["data"]["email"]
            assert body["user"]["name"] == registered_user["data"]["name"]
            assert body["accessToken"].startswith("Bearer ")
            assert body["refreshToken"]

    @allure.title("Вход с неверным логином и паролем")
    def test_login_with_invalid_credentials(self, api_session, user_data):
        invalid_credentials = {
            "email": f"invalid_{user_data['email']}",
            "password": "WrongPassword123!",
        }

        with allure.step("Отправить неверные данные для входа"):
            response = api_session.post(
                f"{BASE_URL}{LOGIN_ENDPOINT}",
                json=invalid_credentials,
            )

        with allure.step("Проверить отказ в авторизации"):
            assert response.status_code == 401
            assert response.json()["success"] is False
            assert (
                response.json()["message"]
                == "email or password are incorrect"
            )
