# Diplom_2

API-автотесты для сервиса «Звёздный бургер».

## Используемые библиотеки

- pytest
- requests
- allure-pytest

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Запуск тестов

```bash
python -m pytest -v
```

## Allure-отчёт

Создать результаты тестов и HTML-отчёт:

```bash
python -m pytest --alluredir=allure-results --clean-alluredir
allure generate allure-results --clean -o allure-report
allure open allure-report
```

## Покрытые сценарии

- Успешная регистрация нового пользователя.
- Повторная регистрация пользователя.
- Регистрация без обязательного поля.
- Вход под существующим пользователем.
- Вход с неверными логином и паролем.
- Создание заказа с авторизацией и ингредиентами.
- Создание заказа без авторизации.
- Создание заказа без ингредиентов.
- Создание заказа с неверным ID ингредиента.
