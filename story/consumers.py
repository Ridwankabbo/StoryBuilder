import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Story, Sentence
from .serializers import StorySentenceSerializer

class StoryConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.story_id = self.scope['url_route']['kwargs']['story_id']
        
        story = await database_sync_to_async(Story.objects.get)(pk=self.story_id)
        user = self.scope['user']
        
        is_allowed = (
            user.is_authenticated and 
            (user == story.created_by or await database_sync_to_async(story.contributors.filter)(id=user.id).exists())
            
        )
        
        if not is_allowed:
            await self.close(code=4003)
            return
        
        self.room_group_name = f"story_{self.story_id}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        await self.send(text_data=json.dumps({
            "type": "story connected",
            'sotry_id':self.story_id
        }))
        
    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )        
        
    async def receive(self, text_data = None, bytes_data = None):
        # Optional: Handle incomming messages
        pass
    
    async def on_new_sentence(self, event):
        sentence = event['sentence']
        await self.send(text_data=json.dumps({
            "type": "sentence",
            "sentence": sentence
        }))
    async def on_sentence_change(self, envent):
        sentence = envent['sentence']
        await self.send(text_data=json.dumps({
            "type":"sentence",
            "sentence":sentence
        }))