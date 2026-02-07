from django.shortcuts import render
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
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

