# models.py
from django.db import models
from django.utils import  timezone
import math

class Ship(models.Model):
    x = models.FloatField(default=0)  # X координата центра корабля
    y = models.FloatField(default=0)  # Y координата центра корабля
    width = models.FloatField(default=10)  # Ширина корабля
    length = models.FloatField(default=4)  # Длина корабля
    speed = models.FloatField(default=0)  # Скорость в м/с
    direction = models.FloatField(default=0)  # Направление в градусах
    last_update = models.DateTimeField(default=timezone.now)
    

    def update_position(self):
        now = timezone.now()
        time_elapsed = (now - self.last_update).total_seconds()

        print(f"Время, прошедшее с последнего обновления: {time_elapsed} секунд")
        print(f"Текущая скорость: {self.speed}, текущее направление: {self.direction}")

        if self.speed > 0:
            radian_direction = math.radians(self.direction)
            distance_moved = time_elapsed * self.speed
            print(f"Пройденное расстояние: {distance_moved}")

            self.x += round(distance_moved * math.cos(radian_direction), 10)  # Округление до 10 десятичных знаков
            self.y += round(distance_moved * math.sin(radian_direction), 10)
            print(f"Новые координаты: x = {self.x}, y = {self.y}")

        
        print(f"Обновленное время последнего обновления: {self.last_update}")

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


    # def save(self, *args, **kwargs):
    #     # Вызываем update_position без принудительного обновления
    #     self.update_position()
    #     super().save(*args, **kwargs)  