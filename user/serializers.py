from rest_framework import serializers
from .models import User
from .utils import generateOTP


""" ********************** User registration serializer *************************** """
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        
    def create(self, validate_data):
            
        try:
            user = User.objects.create_user(
            email = validate_data.get('email'),
            username = validate_data.get('username'),
            password = validate_data.get('password')
            )
            verification_otp = generateOTP()
            print('verification otp', verification_otp)
            user.otp=verification_otp
            user.save()
            # print('verificatin_otp', user.otp)
        except AttributeError:
            raise ValueError(
                {"detail":"otp not found"}
            )
                
        return user
    
    
""" ************************* OTP verification serializer **************************** """
class OtpVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    
""" ************************ Login verification serializer *************************"""
class LoginVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
""" ************************** Forgot password serializer ************************* """
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
""" *************************** Reset password serializer *************************** """
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    password = serializers.CharField()
    
    
        
""" 
    ============================================
        Custom token obtain pair serializer
    ============================================
"""

<<<<<<< HEAD
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework import exceptions
from django.contrib.auth import authenticate

class CustomTokenObtainPariSerializer(TokenObtainSerializer):
=======
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from django.contrib.auth import authenticate

class CustomTokenObtainPariSerializer(TokenObtainPairSerializer):
>>>>>>> development
    username_field = 'email'
    
    def validate(self, attrs):
        email  = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if not user:
                raise exceptions.AuthenticationFailed("No active account found with the given credentials")
            if not user.is_active:
                raise exceptions.AuthenticationFailed("Account isn't active")
<<<<<<< HEAD
            else:
                raise exceptions.AuthenticationFailed("must include email and password")
=======
        else:
            raise exceptions.AuthenticationFailed("must include email and password")
>>>>>>> development
        
        return super().validate(attrs) 