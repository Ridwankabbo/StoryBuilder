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
from .serializers import StoryWithContributiorSerializer
class StoryDetails(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        story_id = request.data.get('story_id')
        story = Story.objects.get(id=story_id)
        serializer = StoryWithContributiorSerializer(story)
        return Response(serializer.data)

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
    
    def post(self, request):
        story_id = request.data.get('story_id')
        story = Story.objects.get(pk=story_id)
        submitted_version = request.data.get('version')
        
        if request.user != story.created_by and request.user not in story.contributors.all():
            return Response({
                "response": "You are not a contributor of the story"
            })
        
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
            
                

"""    
    ====================================
        Story Contributor Request view
    ====================================
"""
from .serializers import StoryContributionRequestSerializer
from .models import StoriColaborationRequest
class ContirbuterRequestView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        sotry_id = request.data.get('story_id')
        story = get_object_or_404(Story, pk=sotry_id)
        print(story)
        requester = story.story_requestes.filter(request_status='Pending')
        print(requester)
        serializer = StoryContributionRequestSerializer(requester, many=True)
        # print(serializer)
        
        return Response(serializer.data)
    
    def post(self, request):
        story = get_object_or_404(Story, pk=request.data.get('story_id'))
        
        if StoriColaborationRequest.objects.filter(story=story.id, requester=request.user).exists():
            return Response({
                "response": "Request already send"
            })
        if request.user == story.created_by:
            return Response({
                "response" : "Creator can't request for contribute"
            })
        
        contoibution_request = StoriColaborationRequest.objects.create(
            story = story,
            requester = request.user
        )
        
        return Response(StoryContributionRequestSerializer(contoibution_request).data)