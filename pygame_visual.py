import pygame
import requests
import time

# Настройки экрана
WIDTH, HEIGHT = 800, 600

# Адрес API
BASE_URL = "http://localhost:8000/ships/"

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Визуализация корабля")
current_ship_id = 1 
def get_ship_data(ship_id):
    """ Получение данных корабля с API """
    try:
        response = requests.get(f"{BASE_URL}{ship_id}/")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка получения данных: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None

def draw_ship(screen, ship_data):
    x = WIDTH / 2
    y = HEIGHT / 2
    width = ship_data['width']*10
    length = ship_data['length']*10

    # Создаем достаточно большую поверхность для вмещения корабля при любом угле поворота
    max_dim = int(max(width, length) * (2 ** 0.5))  # Диагональ прямоугольника
    ship_surface = pygame.Surface((max_dim, max_dim), pygame.SRCALPHA)  # Используем SRCALPHA для прозрачного фона

    # Рисуем корабль на этой поверхности, центрируя его
    ship_rect = pygame.Rect((max_dim - length) // 2, (max_dim - width) // 2, length, width)
    ship_surface.fill((0, 0, 255), ship_rect)

    # Поворачиваем поверхность с кораблем
    rotated_ship = pygame.transform.rotate(ship_surface, -ship_data['direction'])

    # Получаем новый прямоугольник после поворота
    ship_rect = rotated_ship.get_rect(center=(x, y))

    # Отрисовываем повернутый корабль на экране
    screen.blit(rotated_ship, ship_rect.topleft)


def draw_text(screen, text, position, font_size=20, color=(0, 0, 0)):
    """ Отрисовка текста на экране """
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Главный цикл программы
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current_ship_id += 1  # Переключение на следующий корабль
            elif event.key == pygame.K_DOWN:
                current_ship_id = max(1, current_ship_id - 1)  # Переключение на предыдущий корабль


    # Получаем данные корабля
    ship_data = get_ship_data(current_ship_id)  # Используем ID корабля 1 для примера
    if ship_data:
        screen.fill((255, 255, 255))  # Очищаем экран
        draw_ship(screen, ship_data)  # Рисуем корабль

        # Отображаем информацию о корабле
        info_text = f"Координаты: ({ship_data['x']}, {ship_data['y']}), Скорость: {ship_data['speed']}, Направление: {ship_data['direction']}, SHIP № {current_ship_id}"
        draw_text(screen, info_text, (10, 10))

        pygame.display.flip()  # Обновляем экран

    time.sleep(1)  # Задержка для ограничения количества запросов к API

pygame.quit()
