# chat/consumers.py
import json
from unidecode import unidecode
from channels.generic.websocket import AsyncWebsocketConsumer


class KakaoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['browser_id']
        self.room_group_name = u'kakao_%s' % unidecode(self.room_name)
        print("connection checker")
        print(self.room_group_name)
        # Join room group
        await self.channel_layer.group_add(
            unidecode(self.room_group_name),
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat',
                'message': message,
                'username': username
            }
        )

    async def kakao_login(self, event):
        token = event['token']
        print(token)
        await self.send(text_data=json.dumps(event))

    async def chat(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'author': username,
            'message': message,
        }))
