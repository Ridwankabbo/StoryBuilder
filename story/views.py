from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (
    StorySerializer,
)
from .models import Story, Sentence
# Create your views here.


class StoryListView(APIView):
    
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        stories = Story.objects.all()
        serializer = StorySerializer(stories, many=True)
        return Response({serializer.data})
    
    def post(self, request):
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            story = serializer.save(created_by=request.user)
            return Response(StorySerializer(story).data)
        return Response(serializer.errors)        