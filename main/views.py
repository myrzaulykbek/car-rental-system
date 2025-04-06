from django.http import HttpResponse
from rest_framework import viewsets
from .models import Car, Rental
from .serializers import CarSerializer, RentalSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CarFilter, RentalFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

def home(request):
    return HttpResponse("Добро пожаловать в систему аренды автомобилей!")

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter
class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.select_related('user', 'car')
    serializer_class = RentalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RentalFilter

    @action(detail=True, methods=['delete'])
    def cancel_rental(self, request, pk=None):
        rental = self.get_object()
        rental.status = 'canceled'
        rental.save()
        return Response({'status': 'Rental canceled'}, status=status.HTTP_200_OK)