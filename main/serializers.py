# serializers.py
from rest_framework import serializers
from .models import Car, Rental
from django.contrib.auth.models import User

def is_car_available(car, start_date, end_date):
    overlapping_rentals = Rental.objects.filter(
        car=car,
        status__in=['pending', 'active'],
        start_date__lt=end_date,
        end_date__gt=start_date
    )
    return not overlapping_rentals.exists()


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'year', 'price_per_day', 'is_available']

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['id', 'user', 'car', 'start_date', 'end_date', 'status']

    def validate(self, data):
        car = data['car']
        start_date = data['start_date']
        end_date = data['end_date']

        if not is_car_available(car, start_date, end_date):
            raise serializers.ValidationError("Этот автомобиль уже забронирован на выбранные даты.")
        return data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
