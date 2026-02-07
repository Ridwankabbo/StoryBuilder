from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
class Story(models.Model):
    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    version = models.PositiveIntegerField(default=1)
    last_update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} last update:{self.last_update} created_at:{self.created_at}"
    
    
class Sentence(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='sentence')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return f"{self.story.title} - sentence {self.order}"
