# serializers.py
from rest_framework import serializers

from .models import Ship, Planet


class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = ['id', 'x', 'y', 'speed', 'direction', 'length', "width", 'health']


class PlanetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planet
        fields = ['id', 'x', 'y', 'food', 'water', 'fuel', 'oxygen']
