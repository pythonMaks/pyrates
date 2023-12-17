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
    
    def update_position(self, new_speed=None, new_direction=None):
        now = timezone.now()
        time_elapsed = (now - self.last_update).total_seconds()
        if self.speed == 0 and (new_speed is None or new_speed == 0):
            self.last_update = now
            return
        # Вычисление движения на основе текущей скорости и направления
        radian_direction = math.radians(self.direction)
        distance_moved = time_elapsed * self.speed
        self.x += distance_moved * math.cos(radian_direction)
        self.y += distance_moved * math.sin(radian_direction)

        # Обновляем last_update и параметры движения
        self.last_update = now
        if new_speed is not None:
            self.speed = new_speed
        if new_direction is not None:
            self.direction = new_direction

    def move(self, new_angle, new_speed):
        # Сначала обновляем позицию с текущими параметрами
        self.update_position(new_speed=new_speed, new_direction=new_angle)

        # Сохраняем изменения
        self.save()

    def scan(self, scan_angle):
        # Добавим здесь логику сканирования
        pass


    # def save(self, *args, **kwargs):
    #     # Вызываем update_position без принудительного обновления
    #     self.update_position()
    #     super().save(*args, **kwargs)  