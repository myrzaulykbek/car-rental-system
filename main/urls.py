from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, home

router = DefaultRouter()
router.register(r'cars', CarViewSet, basename="car")

urlpatterns = [
    path('', home, name='home'),
    path('api/', include(router.urls)),
]
