
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action, api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import  Rental
from .serializers import CarSerializer, RentalSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CarFilter, RentalFilter
from django.shortcuts import  redirect , get_object_or_404
from .decorators import admin_required, client_required
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .forms import CarForm
from .models import Payment
from .serializers import PaymentSerializer

from .models import  Booking
from datetime import datetime
from django.db.models import Avg
from .forms import ReviewForm


from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.db.models import Avg
from .models import Car, Booking
from .forms import ReviewForm


@login_required
def car_list(request):
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Базовый запрос: доступные машины
    cars = Car.objects.filter(is_available=True).prefetch_related('reviews')
    for car in cars:
        for review in car.reviews.all():
            review.stars_full = [1] * review.rating  # Полные звезды
            review.stars_empty = [1] * (5 - review.rating)  # Пустые звезды

    # Фильтрация по категории
    if category:
        cars = cars.filter(category=category)

    # Фильтрация по датам аренды
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            booked_car_ids = Booking.objects.filter(
                start_date__lte=end,
                end_date__gte=start
            ).values_list('car_id', flat=True)
            cars = cars.exclude(id__in=booked_car_ids)
        except ValueError:
            pass  # если неправильная дата, игнорируем

    # Обработка формы отзыва
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            car = get_object_or_404(Car, id=request.POST.get('car_id'))
            review = form.save(commit=False)
            review.car = car
            review.user = request.user
            review.save()

            # Пересчитываем рейтинг и количество отзывов
            car.reviews_count = car.reviews.count()
            car.reviews_avg = car.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
            car.save()

            return redirect('car_list')
    else:
        form = ReviewForm()

    context = {
        'cars': cars,
        'category': category,
        'start_date': start_date,
        'end_date': end_date,
        'form': form,
        'year': datetime.now().year,
    }
    return render(request, 'main/car_list.html', context)

def client_home(request):
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    cars = Car.objects.filter(is_available=True)

    if category:
        cars = cars.filter(category=category)

    # Фильтр по дате аренды — можно позже доработать

    return render(request, 'client_home.html', {'cars': cars})








class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


def book_car(request, car_id):
    car = Car.objects.get(id=car_id)
    if car.is_available:
        car.is_available = False
        car.save()
    return redirect('car_list')

def home_view(request):
    if request.user.is_authenticated:
        return redirect('car_list')  # редирект на car_list, если пользователь уже авторизован

    return render(request, 'main/welcome.html')



def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('car_list')  # После добавления перенаправить на список машин
    else:
        form = CarForm()

    return render(request, 'add_car.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Перенаправление после входа
        else:
            return render(request, 'main/login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'main/login.html')


def add_car(request):
    return HttpResponse("Здесь будет форма добавления машины.")


from django.shortcuts import render
from .models import Car

from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')








@login_required
def rent_car(request, car_id):
    car = Car.objects.get(id=car_id)
    return render(request, 'rent_car.html', {'car': car})

@admin_required
def admin_dashboard(request):
    return render(request, 'main/admin_dashboard.html')


@client_required
def client_dashboard(request):
    return render(request, 'main/client_dashboard.html')
def home(request):
    return HttpResponse("Добро пожаловать в систему аренды автомобилей!")

# Представление для регистрации
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"error": "Все поля обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем пользователя
        user = User.objects.create_user(username=username, email=email, password=password)

        # Создаем токен для нового пользователя
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


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

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        rental = self.get_object()
        rental.status = 'active'
        rental.save()
        return Response({'status': 'Rental activated'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        rental = self.get_object()
        rental.status = 'completed'
        rental.save()
        return Response({'status': 'Rental completed'}, status=status.HTTP_200_OK)




class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})



from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required

@login_required
def booking_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if not car.is_available:
        return render(request, 'main/booking_unavailable.html', {'car': car})

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            booking.save()

            car.is_available = False
            car.save()
            return redirect('booking_success')


    else:
        form = BookingForm()

    return render(request, 'main/booking_form.html', {'form': form, 'car': car})


def booking_success(request):
    return render(request, 'main/booking_success.html')