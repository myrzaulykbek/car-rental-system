# serializers.py
from rest_framework import serializers
from .models import Car, Rental

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'year', 'price_per_day', 'is_available']

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['id', 'user', 'car', 'start_date', 'end_date', 'status']
