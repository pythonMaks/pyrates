import requests

# URL API для стрельбы корабля
BASE_URL = "http://localhost:8000/ships/"
SHIP_ID = 6  # Пример идентификатора корабля, который будет стрелять

# Параметры выстрела
shoot_params = {
    'power': 740,        # Сила выстрела
    'vertical_angle': 47  # Вертикальный угол выстрела
}

# Отправляем POST-запрос для стрельбы
response = requests.post(f"{BASE_URL}{SHIP_ID}/shoot/", json=shoot_params)

if response.status_code == 200:
    print("Ответ сервера на запрос стрельбы:", response.json())
else:
    print("Ошибка при отправке запроса на стрельбу:", response.status_code)
