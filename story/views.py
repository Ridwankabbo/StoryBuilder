from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import (
    StorySerializer,
    StorySentenceSerializer
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

""" 
    ===============================
        Add sentence serializer
    ===============================
"""
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
class AddSentence(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        story = Story.objects.get(pk=pk)
        sumitted_version = request.data.get('version')
        
        if not sumitted_version:
            return Response({
                'response':'You must send the current version number'
            })
        if int(sumitted_version) != story.version:
            return Response({
                'response':'Conflict: story was updated by someone else. please refresh',
                'current_version':story.version
            })
            
        with transaction.atomic():
            last_order = story.sentence.count() + 1 
            serializer = StorySentenceSerializer(data={
                'text':request.data.get('text'),
                'order' : last_order + 1
            })
            if serializer.is_valid():
                sentence = serializer.save(
                    story = story,
                    author = request.user 
                )
                
                chanel_layer = get_channel_layer()
                async_to_sync(chanel_layer.group_send)(
                    f"story_{story.id}",
                    {
                        "type": "on_new_sentence",
                        "sentence": StorySentenceSerializer(sentence).data,
                        "new_version": story.version + 1  # signal already incremented
                    }
                )
                
            
                return Response(StorySentenceSerializer(sentence).data)
            return Response(serializer.errors)
            
        
        
    
        
                    