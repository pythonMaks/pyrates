# serializers.py
from rest_framework import serializers
from .models import Ship

class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = ['id', 'x', 'y', 'speed', 'direction']
