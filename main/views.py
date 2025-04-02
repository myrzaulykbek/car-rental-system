from django.http import HttpResponse
from rest_framework import viewsets
from .models import Car
from .serializers import CarSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CarFilter

def home(request):
    return HttpResponse("Добро пожаловать в систему аренды автомобилей!")

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter