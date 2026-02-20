from rest_framework import serializers
from .models import Story, Sentence, StoriColaborationRequest

"""    
    =================================
        Story Sentence Serializer
    =================================
"""

class StorySentenceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sentence
        fields = ['text', 'order']


"""    
    ===========================================
        Story conlaboration request serializer
    ===========================================
"""
class StoryContributionRequestSerializer(serializers.ModelSerializer):
    requester = serializers.ReadOnlyField(source='requester.username')
    story_title = serializers.ReadOnlyField(source = 'story.title')
    
    class Meta:
        model = StoriColaborationRequest
        fields = ['id', 'requester', 'story_title', 'request_status', 'requested_at']
   
"""    
    =======================================
        Story with contribution serializer
    =======================================
"""   
class StoryWithContributorsSerializer(serializers.ModelSerializer):
    contributors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='username'
    )
    contribution_requestes = StoryContributionRequestSerializer(many=True, read_only=True)
    
    class Meta:
        model = Story
        fields = [ 'id', 'title', 'created_by', 'contributors', 'contribution_requestes']  


"""    
    =================================
        Story Serializer
    =================================
"""

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'title']
        


