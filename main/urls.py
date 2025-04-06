from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, home, car_list, add_car

router = DefaultRouter()
router.register(r'cars', CarViewSet, basename='car')

urlpatterns = [
    path('', home, name='home'),
    path('cars/', car_list, name='car_list'),
    path('cars/add/', add_car, name='add_car'),
    path('api/', include(router.urls)),
]
