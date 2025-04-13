
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action, api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import  Rental
from .serializers import CarSerializer, RentalSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CarFilter, RentalFilter
from django.shortcuts import  redirect
from .decorators import admin_required, client_required
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import CarForm


from .models import Payment
from .serializers import PaymentSerializer

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

def home_view(request):
    cars = Car.objects.all()  # Получаем все автомобили
    return render(request, 'main/home.html', {'cars': cars})




@login_required
def car_list(request):
    cars = Car.objects.all()
    return render(request, 'main/car_list.html', {'cars': cars})

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
