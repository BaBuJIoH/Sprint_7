import requests
from utils import register_new_courier, delete_courier, BASE_URL

class TestCourierLogin:

    def setup_method(self):
        # Создаем нового курьера перед каждым тестом
        self.new_courier = register_new_courier()

    def teardown_method(self):
        # Удаляем курьера после каждого теста
        if self.new_courier:
            login_payload = {"login": self.new_courier["login"], "password": self.new_courier["password"]}
            response = requests.post(f'{BASE_URL}/courier/login', data=login_payload)
            courier_id = response.json().get('id')
            if courier_id:
                delete_courier(courier_id)

    def test_login_courier(self):
        # Тестируем успешный логин
        login_payload = {"login": self.new_courier["login"], "password": self.new_courier["password"]}
        response = requests.post(f'{BASE_URL}/courier/login', data=login_payload)
        assert response.status_code == 200, "Ошибка при логине"
        assert response.json().get('id'), "Успешный логин не возвращает id"

    def test_login_with_wrong_password(self):
        # Тестируем логин с неправильным паролем
        login_payload = {"login": self.new_courier["login"], "password": "wrongpassword"}
        response = requests.post(f'{BASE_URL}/courier/login', data=login_payload)
        assert response.status_code == 404, "Неправильный пароль не вызывает ошибку"

    def test_login_with_missing_fields(self):
        # Тестируем логин без пароля
        login_payload = {"login": self.new_courier["login"]}
        response = requests.post(f'{BASE_URL}/courier/login', data=login_payload)
        assert response.status_code == 400, "Не возвращается ошибка при отсутствии поля"
