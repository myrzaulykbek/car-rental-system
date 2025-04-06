from django.http import HttpResponse
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Car
from .serializers import CarSerializer

def home(request):
    return HttpResponse("Добро пожаловать в систему аренды автомобилей!")

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.filter(is_available=True)  # Фильтр: только доступные авто
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]  # Доступ только для авторизованных пользователей
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]  # Фильтрация и поиск
    ordering_fields = ["price_per_day", "year"]  # Сортировка по цене или году выпуска
    search_fields = ["brand", "model"]  # Поиск по марке и модели

