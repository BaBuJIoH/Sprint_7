import requests
from utils import register_new_courier, delete_courier

class TestCourierCreation:
    def setup_method(self):
        # Подготовка данных перед тестом
        self.new_courier = register_new_courier()

    def teardown_method(self):
        # Удаление данных после теста
        if self.new_courier:
            courier_id = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                       data={"login": self.new_courier["login"], "password": self.new_courier["password"]}).json().get('id')
            delete_courier(courier_id)

    def test_create_courier(self):
        assert self.new_courier is not None, "Курьер не был создан"
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                 data={"login": self.new_courier["login"], "password": self.new_courier["password"]})
        assert response.status_code == 200, "Курьер не может войти после создания"
        assert response.json().get('id'), "Успешная регистрация не возвращает id"

    def test_create_same_courier(self):
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=self.new_courier)
        assert response.status_code == 409, "Можно создать курьера с существующим логином"

    def test_create_courier_with_missing_fields(self):
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier',
                                 data={"login": "testlogin", "password": "testpassword"})
        assert response.status_code == 400, "Не возвращается ошибка при отсутствии обязательного поля"
