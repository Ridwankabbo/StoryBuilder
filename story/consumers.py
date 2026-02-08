import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Story, Sentence
from .serializers import StorySentenceSerializer

class StoryConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.story_id = self.scope['url_route']['kwargs']['story_id']
        self.room_group_name = f"story_{self.story_id}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
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