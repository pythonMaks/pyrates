# views.py
from rest_framework import viewsets
from .models import Ship
from .serializers import ShipSerializer
from rest_framework.response import Response

class ShipViewSet(viewsets.ModelViewSet):
    queryset = Ship.objects.all()
    serializer_class = ShipSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.update_position()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)