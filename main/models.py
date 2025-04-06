from django.db import models

class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    price_per_day = models.FloatField()
    is_available = models.BooleanField(default=True)
    vin_number = models.CharField(max_length=17, unique=True, null=True, blank=True)


    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
