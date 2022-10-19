import asyncio
import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *  # new import
from .serializers import *
from channels.exceptions import StopConsumer


class UserInboxConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.chat_rooms = []

    def connect(self):
        try:
            self.user = self.scope['user']
            self.accept()
            self.chat_rooms = self.user.room_set.all()
            Client.objects.filter(user=self.user).delete()
            Client.objects.create(channel_name=self.channel_name, user=self.user)
            for room in self.chat_rooms:
                async_to_sync(self.channel_layer.group_add)(
                    room.group_name,
                    self.channel_name
                )
        except:
            raise StopConsumer

    def disconnect(self, code):
        for room in self.chat_rooms:
            async_to_sync(self.channel_layer.group_discard)(
                room.group_name,
                self.channel_name
            )
        Client.objects.filter(channel_name=self.channel_name).delete()
        raise StopConsumer

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message_type = data.get('message_type')
        if message_type == 0:
            room_id = data.get('room_id')
            content = data.get('content')
            try:
                room = Room.objects.get(pk=room_id, user=self.user.id)
            except:
                pass
            else:
                message = Message.objects.create(creator=self.user, room=room, content=content)
                avatar = ""
                if self.user.avatar:
                    avatar = self.user.avatar.url
                async_to_sync(self.channel_layer.group_send)(
                    room.group_name,
                    {
                        "type": "chat_message",
                        "message_type": message_type,
                        "content": message.content,
                        "creator_first_name": self.user.first_name,
                        "creator_last_name": self.user.last_name,
                        "creator_avatar": avatar,
                        "creator_id": self.user.id,
                        "room_id": room.id,
                        "created_date": str(message.created_date)
                    }
                )
        elif message_type == 1:
            pass

    def chat_message(self, event):
        self.send(text_data=json.dumps(event, ensure_ascii=False))

    def system_message(self, event):
        self.chat_message(event)


class ChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.chat_rooms = None

    async def connect(self):
        self.user = self.scope['user']
        self.chat_rooms = await database_sync_to_async(self.user.room_set.all)()
        await self.accept()
        await database_sync_to_async(Client.objects.filter(user=self.user).delete)()
        await database_sync_to_async(Client.objects.create)(channel_name=self.channel_name, user=self.user)
        async for room in self.chat_rooms:
            await self.channel_layer.group_add(room.group_name, self.channel_name)

    async def disconnect(self, code):
        async for room in self.chat_rooms:
            await self.channel_layer.group_discard(room.group_name, self.channel_name)
        await database_sync_to_async(Client.objects.filter(user=self.user).delete)()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        data = json.loads(text_data)
        message_type = data.get('message_type')
        if message_type == 0:
            room_id = data.get('room_id')
            content = data.get('content')
            try:
                room = await database_sync_to_async(Room.objects.get)(pk=room_id)
            except:
                pass
            else:
                message = await database_sync_to_async(Message.objects.create)(creator=self.user, room=room, content=content)
                await self.channel_layer.group_send(
                    room.group_name,
                    {
                        "type": "chat_message",
                        "message_type": message_type,
                        "creator_id": self.user.id,
                        "creator_first_name": self.user.first_name,
                        "creator_last_name": self.user.last_name,
                        "creator_avatar": [self.user.avatar.url if self.user.avatar else ""],
                        "room_id": room.id,
                        "content": message.content
                    }
                )
        elif message_type == 1:
            pass

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event, ensure_ascii=False))

