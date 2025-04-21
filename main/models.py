from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Менеджер пользователя
class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(username, email, password, **extra_fields)


# Модель автомобиля
class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


# Модель пользователя
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    objects = UserManager()


# Модель аренды
class Rental(models.Model):
    PENDING = 'pending'
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Rental: {self.user.username} -> {self.car} ({self.start_date} - {self.end_date})"


# Модель платежа за аренду
class Payment(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ], default='pending')

    def __str__(self):
        return f"Payment: {self.rental} - {self.amount} ({self.status})"


# Отдельная модель для ручных платежей (Kaspi, Halyk и т.д.)
class ManualPayment(models.Model):
    PAYMENT_METHODS = [
        ('kaspi', 'Kaspi'),
        ('halyk', 'Halyk Bank'),
        ('cash', 'Cash'),
        ('stripe', 'Stripe'),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} | {self.get_method_display()} | {self.amount} ₸"
