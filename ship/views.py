# views.py
from rest_framework import viewsets
from .models import Ship
from .serializers import ShipSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import render

class ShipViewSet(viewsets.ModelViewSet):
    queryset = Ship.objects.all()
    serializer_class = ShipSerializer

    def get_queryset(self):
        # Всегда возвращаем свежий queryset из базы данных
        return Ship.objects.all()

    def list(self, request, *args, **kwargs):
        updated_ships = []
        for ship in self.get_queryset():  # Используем self.get_queryset() здесь
            ship.update_position()  # Вычисляем новые координаты без сохранения
            updated_ships.append(ship)

        # Сериализуем обновленные данные кораблей для ответа
        serializer = self.get_serializer(updated_ships, many=True)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.update_position()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        speed = request.data.get('speed')
        direction = request.data.get('direction')

        if speed is not None and direction is not None:
            instance.move(float(direction), float(speed))
        else:
            # обработка случая, когда не все параметры предоставлены
            pass

        return Response(self.get_serializer(instance).data)
    
    @action(detail=True, methods=['post'])
    def shoot(self, request, pk=None):
        ship = self.get_object()
        power = request.data.get('power')
        vertical_angle = request.data.get('vertical_angle')

        if power is None or vertical_angle is None:
            return Response(
                {"error": "Power and vertical angle are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Вызываем метод shoot у модели корабля один раз
        result = ship.shoot(power=float(power), vertical_angle=float(vertical_angle))
        
        # Включаем координаты попадания в ответ
        response_data = {
            'hit': result['hit'],
            'impact_x': result['impact_x'],
            'impact_y': result['impact_y']
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    
def index(request):
    return render(request, 'ship/index.html')


from .models import Planet
from .serializers import PlanetSerializer  # Предполагается, что вы создали соответствующий сериализатор

class PlanetViewSet(viewsets.ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

    def create(self, request, *args, **kwargs):
        num_planets = int(request.data.get('num_planets', 1))
        for _ in range(num_planets):
            Planet.objects.create()
        return Response({'status': 'Planets created'}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)