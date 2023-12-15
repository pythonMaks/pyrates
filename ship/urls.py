# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ShipViewSet

router = DefaultRouter()
router.register(r'ships', ShipViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
