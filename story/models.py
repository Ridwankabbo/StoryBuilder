from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
class Story(models.Model):
    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    contributors = models.ManyToManyField(User, related_name='contributed_stories', blank=True)
    version = models.PositiveIntegerField(default=1)
    last_update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title}"
    
    
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
    
    
class StoriColaborationRequest(models.Model):
    class RequestStatus(models.TextChoices):
        CANCLED = 'CNLD', 'Cancled'
        ACCEPTED = 'ACD', 'Accepted'
        PENDING = 'PND', 'Pending'
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story_requestes')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_request')
    request_status = models.TextField(choices=RequestStatus.choices, default=RequestStatus.PENDING)
    requested_at = models.DateTimeField(auto_now_add=True)
    responced_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('story', 'requester')
        ordering = ['-requested_at']
        
    def __str__(self):
        return f" User: {self.requester.username} whants to contribute in  {self.story.title}."

