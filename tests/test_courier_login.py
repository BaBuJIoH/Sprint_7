import requests
from utils import register_new_courier, delete_courier

class TestCourierLogin:
    def setup_method(self):
        self.new_courier = register_new_courier()

    def teardown_method(self):
        if self.new_courier:
            courier_id = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                       data={"login": self.new_courier["login"], "password": self.new_courier["password"]}).json().get('id')
            delete_courier(courier_id)

    def test_login_courier(self):
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                 data={"login": self.new_courier["login"], "password": self.new_courier["password"]})
        assert response.status_code == 200, "Ошибка при логине"
        assert response.json().get('id'), "Успешный логин не возвращает id"

    def test_login_with_wrong_password(self):
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                 data={"login": self.new_courier["login"], "password": "wrongpassword"})
        assert response.status_code == 404, "Неправильный пароль не вызывает ошибку"

    def test_login_with_missing_fields(self):
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                 data={"login": self.new_courier["login"]})
        assert response.status_code == 400, "Не возвращается ошибка при отсутствии поля"
