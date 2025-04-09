from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, RentalViewSet, home, register, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views


router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'rentals', RentalViewSet)

urlpatterns = [
    path('cars/', views.car_list, name='car_list'),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('api/', include(router.urls)),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),

    # JWT токены
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
]

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
]
