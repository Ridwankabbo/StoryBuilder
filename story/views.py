from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import (
    StorySerializer,
)
from .models import Story, Sentence
# Create your views here.

""" 
    =======================================
        List all stories + creat storis
    =======================================
"""
class StoryListView(APIView):
    
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        stories = Story.objects.all()
        serializer = StorySerializer(stories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            story = serializer.save(created_by=request.user)
            return Response(StorySerializer(story).data)
        return Response(serializer.errors)
    
""" 
    ========================
        Get story details
    ========================
"""
class StoryDetails(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        serializer = StorySerializer(story)
        return Response(serializer.data)
        
                    