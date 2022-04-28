# chat/consumers.py
import json
from asgiref.sync import sync_to_async
from unidecode import unidecode
from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps
from channels.auth import logout
from pprint import pprint


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        target = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = u'user_%s' % unidecode(self.room_name)
        print(f"connection checker {self.room_group_name}")
        # Join room group
        await self.channel_layer.group_add(
            unidecode(self.room_group_name),
            self.channel_name
        )

        await self.accept()
        data = {
            "message": f"Connected in User {self.room_name}"
        }
        await self.receive(json.dumps(data))

    async def disconnect(self, close_code):
        # Leave room group
        await logout(self.scope)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(text_data)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'connected',
                'message': message,
            }
        )

    async def connected(self, event):
        await self.send(text_data=json.dumps(event))

    async def order(self, event):
        await self.send(text_data=json.dumps(event))


class UserNotifyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        target = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = u'personal_notify_%s' % unidecode(
            self.room_name)
        print(f"connection checker {self.room_group_name}")
        # Join room group
        await self.channel_layer.group_add(
            unidecode(self.room_group_name),
            self.channel_name
        )

        await self.accept()
        data = {
            "message": f"Connected in User {self.room_name}"
        }
        await self.receive(json.dumps(data))

    async def disconnect(self, close_code):
        # Leave room group
        await logout(self.scope)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(text_data)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'connected',
                'message': message,
            }
        )

    async def connected(self, event):
        await self.send(text_data=json.dumps(event))

    async def order(self, event):
        await self.send(text_data=json.dumps(event))


class DMConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = u'chat_%s' % unidecode(
            self.room_name)
        print(f"connection checker {self.room_group_name}")
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
        user_id = int(text_data_json['user_id'])
        await sync_to_async(apps.get_model('todos', 'dm').objects.create)(
            author_id=user_id, message=message, room_name=self.room_group_name
        )
        # Send message to room group
        if message and username:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat',
                    'username': username,
                    'message': message,
                }
            )

    async def chat(self, event):
        await self.send(text_data=json.dumps(event))

    async def order(self, event):
        await self.send(text_data=json.dumps(event))
