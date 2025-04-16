from django.urls import  include
from rest_framework.routers import DefaultRouter
from .views import  RentalViewSet,  register, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import home_view, register_view

from django.conf import settings
from django.conf.urls.static import static

from .views import CarViewSet, PaymentViewSet, home



router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'payments', PaymentViewSet)  # добавили платежи




router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'payments', PaymentViewSet)  # добавили платежи






router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'rentals', RentalViewSet)



urlpatterns = [
    path('register/', register_view, name='register'),
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('', views.home_view, name='home'),  # Главная страница
    path('car_list/', views.car_list, name='car_list'),  # Список машин
    path('', home_view, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('add_car/', views.add_car, name='add_car'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),


    path('', home, name='home'),
    path('api/', include(router.urls)),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),

    # JWT токены
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



urlpatterns += [
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='main/password_reset.html'),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'),
         name='password_reset_complete'),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
