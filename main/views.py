from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Car

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .serializers import CarSerializer


def home(request):
    return HttpResponse("Добро пожаловать в систему аренды автомобилей!")

# Список машин (HTML)
def car_list(request):
    cars = Car.objects.all()
    return render(request, 'main/car_list.html', {'cars': cars})

# Добавление машины (HTML)
def add_car(request):
    if request.method == 'POST':
        brand = request.POST['brand']
        model = request.POST['model']
        year = request.POST['year']
        price_per_day = request.POST['price_per_day']
        Car.objects.create(brand=brand, model=model, year=year, price_per_day=price_per_day)
        return redirect('car_list')
    return render(request, 'main/add_car.html')

# API: /api/cars/
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.filter(is_available=True)
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["price_per_day", "year"]
    search_fields = ["brand", "model"]
