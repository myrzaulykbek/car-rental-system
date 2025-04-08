from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, RentalViewSet, home, register, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from . import views


router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'rentals', RentalViewSet)

urlpatterns = [
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


