from rest_framework import serializers
from .models import Story, Sentence


class StorySentenceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sentence
<<<<<<< HEAD
        fields = '__all__'
=======
        fields = ['id','text', 'order']
>>>>>>> development

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'title']
        


