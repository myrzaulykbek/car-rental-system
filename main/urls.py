from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, RentalViewSet, home , register # Импортируем views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # Импортируем views для JWT

# Инициализируем маршрутизатор
router = DefaultRouter()

# Регистрируем viewsets
router.register(r'cars', CarViewSet)
router.register(r'rentals', RentalViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),  # Регистрируем маршрут для регистрации
    path('api/', include(router.urls)),  # Подключаем маршруты для API
    # Маршруты для получения и обновления токенов
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
