import requests
import random
import string

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def register_new_courier(login=None, password=None, first_name=None):
    if not login:
        login = generate_random_string(10)
    if not password:
        password = generate_random_string(10)
    if not first_name:
        first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{BASE_URL}/courier', data=payload)
    if response.status_code == 201:
        return {"login": login, "password": password, "firstName": first_name}
    return None

def delete_courier(courier_id):
    response = requests.delete(f'{BASE_URL}/courier/{courier_id}')
    return response.status_code == 200
