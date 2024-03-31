# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ShipViewSet, index, PlanetViewSet

router = DefaultRouter()
router.register(r'ships', ShipViewSet)
router.register(r'planets', PlanetViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('map/', index)
]
