from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import (
    StorySerializer,
<<<<<<< HEAD
)
from .models import Story, Sentence
=======
    StorySentenceSerializer
)
from .models import Story
>>>>>>> development
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
<<<<<<< HEAD
        
=======

""" 
    ===============================
        Sentence View
    ===============================
"""
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Sentence
from .permissions import IsAuthorOrStoryCreator
class SentenceView(APIView):
    
    permission_classes = [IsAuthenticated, IsAuthorOrStoryCreator]
    
    def get(self, request):
        # Why use get_object_or_404 on Story first? It ensures the story exists before querying sentences.
        story_id = request.data.get('story_id')
        story = get_object_or_404(Story, pk=story_id)
        sentences = Sentence.objects.filter(story=story).order_by('order')  # Fetch all sentences for the story
        serializer = StorySentenceSerializer(sentences, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        story = Story.objects.get(pk=pk)
        submitted_version = request.data.get('version')
        
        if not submitted_version:
            return Response({
                'response':'You must send the current version number'
            })
        if int(submitted_version) != story.version:
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
    
    def patch(self, request):
        sentence_id = request.data.get('sentence_id')
        sentence = get_object_or_404(Sentence, id=sentence_id)
        
        self.check_object_permissions(request, sentence)
        
        story = sentence.story
        submitted_version = request.data.get('version')
        
        if not submitted_version:
            return Response({
                'response':'You must send the current version number'
            })
        if int(submitted_version) != story.version:
            return Response({
                'response':'Conflict: story was updated by someone else. please refresh',
                'current_version':story.version
            })
        
        with transaction.atomic():
            serializer = StorySentenceSerializer(sentence, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                story.version += 1  # Increment for delete too?
                story.save(update_fields=['version'])
                
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"story_{story.id}",
                    {
                        "type":"on_sentence_change",
                        "sentence":StorySentenceSerializer(sentence).data,
                        "new_version":story.version
                    }
                )
                
                return Response(serializer.data)
        return Response(serializer.errors)
                
                
            
    def delete(self, request):
        sentence_id = request.data.get('sentence_id')
        sentence = get_object_or_404(Sentence, pk=sentence_id)
        self.check_object_permissions(request, sentence)
        
        story = sentence.story
        
        with transaction.atomic():
            sentence.delete()
            story.version += 1  # Increment for delete too?
            story.save(update_fields=['version'])
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"story_{story.id}",
                {
                    "type":"on_sentence_change",
                    "sentence":StorySentenceSerializer(sentence).data,
                    "new_version":story.version
                })
            
        return Response({"response":"Sentence deleted success"})
            
                
>>>>>>> development
                    