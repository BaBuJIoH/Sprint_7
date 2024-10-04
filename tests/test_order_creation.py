import requests
import pytest
from utils import BASE_URL

class TestOrderCreation:

    # Параметризация для тестирования создания заказа с разными цветами
    @pytest.mark.parametrize("color, expected_status_code", [
        (["BLACK"], 201),  # Один цвет
        (["GREY"], 201),  # Один цвет
        (["BLACK", "GREY"], 201),  # Два цвета
        (None, 201),  # Без указания цвета
    ])
    def test_create_order(self, color, expected_status_code):
        # Тело запроса для создания заказа
        payload = {}
        if color:
            payload["color"] = color

        # Отправляем запрос на создание заказа
        response = requests.post(f'{BASE_URL}/orders', data=payload)

        # Проверяем, что статус ответа соответствует ожиданиям
        assert response.status_code == expected_status_code, f"Неверный статус при создании заказа с цветом {color}"

        # Проверяем, что в теле ответа есть поле 'track'
        assert response.json().get('track'), "Трек заказа отсутствует в ответе"

    def test_create_order_without_address(self):
        # Пример теста на проверку заказа без обязательных полей (например, без адреса)
        payload = {
            "color": ["BLACK"],
            # Другие поля заказа
        }

        response = requests.post(f'{BASE_URL}/orders', data=payload)

        assert response.status_code == 400, "Должна быть ошибка при отсутствии обязательного поля"
