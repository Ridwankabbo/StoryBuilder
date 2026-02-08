from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Sentence

@receiver(post_save, sender=Sentence)
def increment_story_version(sender, instance, created, **kwargs):
    if created:
        story = instance.story
        story.version += 1
        story.save(update_fields=['version'])