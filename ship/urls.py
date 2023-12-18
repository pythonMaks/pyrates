# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ShipViewSet, index

router = DefaultRouter()
router.register(r'ships', ShipViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('map/', index)
]
