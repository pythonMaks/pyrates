import requests
import time
BASE_URL = "http://localhost:8000/ships/"  # Предполагаем, что ваш сервер запущен локально
SHIP_ID = 1
# Пример идентификатора корабля

def get_ship_data(ship_id):
    """ Получение данных корабля """
    response = requests.get(f"{BASE_URL}{ship_id}/")
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"

def update_ship_data(ship_id, speed, direction):
    """ Обновление параметров движения корабля """
    data = {'speed': speed, 'direction': direction}
    response = requests.patch(f"{BASE_URL}{ship_id}/", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"

# Пример использования
print("Текущие данные корабля:", get_ship_data(SHIP_ID))
print("Обновляем данные корабля...")
updated_data = update_ship_data(SHIP_ID, speed=0.1, direction=38)
print("Обновленные данные корабля:", updated_data)
print("Ожидаем 5 секунд..")
time.sleep(5)
updated_data = get_ship_data(SHIP_ID)
print("Обновленные данные корабля:", updated_data)
