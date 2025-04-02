import django_filters
from .models import Car

class CarFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(field_name='brand', lookup_expr='icontains')
    year__gt = django_filters.NumberFilter(field_name='year', lookup_expr='gt')
    year__lt = django_filters.NumberFilter(field_name='year', lookup_expr='lt')
    price_per_day__lte = django_filters.NumberFilter(field_name='price_per_day', lookup_expr='lte')
    price_per_day__gte = django_filters.NumberFilter(field_name='price_per_day', lookup_expr='gte')

    class Meta:
        model = Car
        fields = ['brand', 'is_available']