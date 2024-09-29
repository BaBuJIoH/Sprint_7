import requests

class TestOrderList:

    def test_get_orders_list(self):
        response = requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders')
        assert response.status_code == 200, "Не удалось получить список заказов"
        assert len(response.json().get('orders', [])) > 0, "Список заказов пуст"
