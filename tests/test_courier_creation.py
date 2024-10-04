import requests
from utils import register_new_courier, delete_courier, BASE_URL

class TestCourierCreation:

    def test_create_courier(self):
        # Создаем нового курьера
        new_courier = register_new_courier()

        # Проверяем, что курьер успешно создан
        assert new_courier is not None, "Курьер не был создан"

        # Проверяем, что курьер может залогиниться
        login_payload = {"login": new_courier["login"], "password": new_courier["password"]}
        login_response = requests.post(f'{BASE_URL}/courier/login', data=login_payload)
        assert login_response.status_code == 200, "Курьер не может залогиниться"
        assert login_response.json().get('id'), "Логин не возвращает id курьера"

        # Удаляем созданного курьера
        courier_id = login_response.json().get('id')
        assert delete_courier(courier_id), "Не удалось удалить курьера"

    def test_create_same_courier(self):
        # Создаем нового курьера
        new_courier = register_new_courier()

        # Проверяем, что курьер успешно создан
        assert new_courier is not None, "Курьер не был создан"

        # Попробуем создать курьера с теми же логином и паролем
        response = requests.post(f'{BASE_URL}/courier', data={
            "login": new_courier["login"],
            "password": new_courier["password"],
            "firstName": new_courier["firstName"]
        })
        assert response.status_code == 409, "Курьер с тем же логином создан повторно"

        # Удаляем созданного курьера
        login_response = requests.post(f'{BASE_URL}/courier/login', data={
            "login": new_courier["login"],
            "password": new_courier["password"]
        })
        courier_id = login_response.json().get('id')
        assert delete_courier(courier_id), "Не удалось удалить курьера"

    def test_create_courier_with_missing_fields(self):
        # Пытаемся создать курьера без логина и пароля
        response = requests.post(f'{BASE_URL}/courier', json={
            "firstName": "testFirstName"
        })
        assert response.status_code == 400, "Не возвращается ошибка при отсутствии логина и пароля"

    def test_create_courier_with_required_fields_only(self):
        # Пытаемся создать курьера только с логином и паролем
        response = requests.post(f'{BASE_URL}/courier', json={
            "login": "testlogin",
            "password": "testpassword"
        })
        assert response.status_code == 201, "Не удается создать курьера только с логином и паролем"
        assert response.json().get('id'), "Успешное создание курьера не возвращает id"

        # Удаляем созданного курьера
        courier_id = requests.post(f'{BASE_URL}/courier/login', json={
            "login": "testlogin",
            "password": "testpassword"
        }).json().get('id')
        assert delete_courier(courier_id), "Не удалось удалить курьера"
