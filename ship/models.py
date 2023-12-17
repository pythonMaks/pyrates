# models.py
from django.db import models


class Ship(models.Model):
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    speed = models.FloatField(default=0)
    direction = models.FloatField(default=0)

    def move(self, angle, speed):
        pass

    def scan(self, scan_angle):
        # Добавим здесь логику сканирования
        pass
