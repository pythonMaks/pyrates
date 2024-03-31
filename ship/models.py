# models.py
import math
import random

from django.db import models
from django.utils import timezone


class Ship(models.Model):
    x = models.FloatField(default=0)  # X координата центра корабля
    y = models.FloatField(default=0)  # Y координата центра корабля
    width = models.FloatField(default=10)  # Ширина корабля
    length = models.FloatField(default=4)  # Длина корабля
    speed = models.FloatField(default=0)  # Скорость в м/с
    direction = models.FloatField(default=0)  # Направление в градусах
    last_update = models.DateTimeField(default=timezone.now)
    health = models.IntegerField(default=100)
    food = models.FloatField(default=100)  # Еда на корабле
    water = models.FloatField(default=100)  # Вода на корабле
    fuel = models.FloatField(default=100)  # Топливо на корабле
    oxygen = models.FloatField(default=100)  # Кислород на корабле

    def update_position(self):
        now = timezone.now()
        time_elapsed = (now - self.last_update).total_seconds()
        self.consume_resources(time_elapsed)
        print(f"Текущая скорость: {self.speed}, текущее направление: {self.direction}")

        if self.speed > 0:
            radian_direction = math.radians(self.direction)
            distance_moved = time_elapsed * self.speed
            print(f"Пройденное расстояние: {distance_moved}")

            self.x += round(distance_moved * math.cos(radian_direction), 10)  # Округление до 10 десятичных знаков
            self.y += round(distance_moved * math.sin(radian_direction), 10)
            print(f"Новые координаты: x = {self.x}, y = {self.y}")

    def move(self, new_angle, new_speed):
        print(f"Изменение скорости и направления: скорость = {new_speed}, направление = {new_angle}")

        # Обновляем позицию с текущими параметрами
        self.update_position()

        # Затем обновляем скорость и направление
        self.speed = new_speed
        self.direction = new_angle
        self.last_update = timezone.now()
        # Сохраняем изменения
        self.save()

    def scan(self, scan_angle):
        # Добавим здесь логику сканирования
        pass

    def shoot(self, power, vertical_angle):
        # Обновляем позицию стреляющего корабля
        self.update_position()

        # Рассчитываем скорость и координаты попадания снаряда
        radian_direction = math.radians(self.direction)
        radian_vertical = math.radians(vertical_angle)
        speed_x = power * math.cos(radian_vertical) * math.cos(radian_direction)
        speed_y = power * math.cos(radian_vertical) * math.sin(radian_direction)
        impact_x = self.x + speed_x
        impact_y = self.y + speed_y

        # Инициализация переменной hit
        hit = False
        # Проверяем попадание по другим кораблям
        for target_ship in Ship.objects.exclude(id=self.id):
            target_ship.update_position()  # Обновляем позицию каждого корабля перед проверкой попадания
            if self._is_hit(target_ship, impact_x, impact_y):
                # Наносим урон кораблю
                target_ship.health -= 50  # Например, снаряд наносит 50 урона
                target_ship.save()
                hit = True  # Записываем факт попадания
                break  # Останавливаем проверку после первого попадания

        return {
            'hit': hit,  # Было ли попадание
            'impact_x': impact_x,  # Координата X точки попадания
            'impact_y': impact_y  # Координата Y точки попадания
        }

    def consume_resources(self, time_elapsed):
        self.food -= time_elapsed
        self.water -= time_elapsed
        self.fuel -= time_elapsed
        self.oxygen -= time_elapsed
        self.save()

    def
        (self, planet):
        if self._is_near(planet):
            self.food += planet.food
            self.water += planet.water
            self.fuel += planet.fuel
            self.oxygen += planet.oxygen
            self.save()

            # Обнуляем ресурсы на планете
            planet.food = 0
            planet.water = 0
            planet.fuel = 0
            planet.oxygen = 0
            planet.save()

    def _is_near(self, planet):
        distance = math.sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)
        return distance < 1  # Например, считаем, что корабль рядом, если расстояние меньше 1


    def _is_hit(self, target_ship, impact_x, impact_y):
        # Проверяем, находится ли точка попадания в пределах корабля
        ship_left = target_ship.x - target_ship.width / 2
        ship_right = target_ship.x + target_ship.width / 2
        ship_top = target_ship.y - target_ship.length / 2
        ship_bottom = target_ship.y + target_ship.length / 2

        return (ship_left <= impact_x <= ship_right) and (ship_top <= impact_y <= ship_bottom)


class RandomFloatField(models.FloatField):
    def pre_save(self, model_instance, add):
        return random.uniform(0, 100)


class Planet(models.Model):
    x = RandomFloatField(default=0)  # X координата планеты
    y = RandomFloatField(default=0)  # Y координата планеты
    food = RandomFloatField(default=0)  # Еда на планете
    water = RandomFloatField(default=0)  # Вода на планете
    fuel = RandomFloatField(default=0)  # Топливо на планете
    oxygen = RandomFloatField(default=0)  # Кислород на планете
