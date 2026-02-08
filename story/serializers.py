from rest_framework import serializers
from .models import Story, Sentence


class StorySentenceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sentence
        fields = '__all__'

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'title']
        


