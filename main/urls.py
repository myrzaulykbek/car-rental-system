from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, RentalViewSet, home  # Импортируем RentalViewSet

# Инициализируем маршрутизатор
router = DefaultRouter()

# Регистрируем viewsets
router.register(r'cars', CarViewSet)
router.register(r'rentals', RentalViewSet)  # Регистрируем RentalViewSet

urlpatterns = [
    path('', home, name='home'),
    path('api/', include(router.urls)),  # Подключаем маршруты
]