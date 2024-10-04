import requests
from utils import BASE_URL

class TestOrderList:

    def test_get_orders_list(self):
        response = requests.get(f'{BASE_URL}/orders')
        assert response.status_code == 200, "Не удалось получить список заказов"
        assert len(response.json().get('orders', [])) > 0, "Список заказов пуст"
