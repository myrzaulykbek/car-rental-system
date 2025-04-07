from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, RentalViewSet, home, register, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'rentals', RentalViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('api/', include(router.urls)),

    # JWT токены
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
]
