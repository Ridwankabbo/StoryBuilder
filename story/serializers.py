from rest_framework import serializers
from .models import Story, Sentence


class StorySentenceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sentence
        fields = ['id','text', 'order']

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'title']
        


