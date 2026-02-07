from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    UserRegistrationSerializer,
    OtpVerificationSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from .models import User
from .utils import generateOTP

# Create your views here.

""" 
    ============================
        Registration view
    ============================
"""
@api_view(['POST'])
def UserRegistrationView(request):
    serializer = UserRegistrationSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        
        return Response(serializer.data)
    return Response(serializer.errors)

""" 
    ===============================
        Otp verification view
    ===============================
"""
@api_view(['POST'])
def OtpVerificationView(request):
    serializer = OtpVerificationSerializer(data = request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        otp = serializer.validated_data.get('otp')
        try:
            user = User.objects.get(email=email)
            if user.otp == otp:
                user.is_active = True
                user.otp = None
                user.save()
                
                return Response({"response": "Account verified successfully"})
            return Response({"response":"Invalid otp"})
        except User.DoesNotExist:
            return Response({"response": "User doesn't exiist"})
        
    return Response(serializer.errors)

""" 
    ============================
        Forgot password view
    ============================
"""
@api_view(['POST'])
def ForgotPasswordView(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        
        try:
            user = User.objects.get(email=email)
            new_verification_otp = generateOTP()
            user.otp = new_verification_otp
            user.save()
            print("new otp:", user.otp)
            
            return Response({'response':'new otp send'})

        except User.DoesNotExist:
            return Response({"response":"User doesn't exist"})
    return Response(serializer.errors)    

""" 
    ==============================
        Reset passsword view
    ==============================
"""
@api_view(['POST'])
def ResetPasswordView(request):
    serializer = ResetPasswordSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        otp = serializer.validated_data.get('otp')
        password = serializer.validated_data.get('password')
        
        try:
            user = User.objects.get(email=email)
            if user.otp == otp:
                user.password = password
                user.otp = None
                user.save()
                
                return Response({"response":"Password successfully reset"})
        except User.DoesNotExist:
            return Response({"response":"User doesn't exist"})
    return Response(serializer.errors)

