from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
urlpatterns = [
    path('register/', views.UserRegistrationView, name='register'),
    path('verify-otp/', views.OtpVerificationView, name='verify-otp'),
    path('forgot-password/', views.ForgotPasswordView, name='forgot-password'),
    path('reset-password/', views.ResetPasswordView, name='reset-password'),
    
    path('login/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
