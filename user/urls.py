from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.UserRegistrationView, name='register'),
    path('verify-otp/', views.OtpVerificationView, name='verify-otp'),
    path('forgot-password/', views.ForgotPasswordView, name='forgot-password'),
    path('reset-password/', views.ResetPasswordView, name='reset-password'),
]
