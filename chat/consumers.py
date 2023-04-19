import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer, JsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from market.serializers import *
from channels.exceptions import StopConsumer
from .tasks import *
from market.models import *
from market.tasks import *
import asyncio
from typing import Any


class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.rooms = []

    def connect(self):
        try:
            self.user = self.scope['user']
            self.accept()
            self.rooms = Room.objects.filter(user=self.user)
            for room in self.rooms:
                async_to_sync(self.channel_layer.group_add)(
                    room.group_name,
                    self.channel_name
                )
        except:
            raise StopConsumer

    def disconnect(self, **kwargs):
        for room in self.rooms:
            async_to_sync(self.channel_layer.group_discard)(
                room.group_name,
                self.channel_name
            )
        raise StopConsumer

    def receive_json(self, content, **kwargs):
        content = content.get('content')
        room_id = content.get('room_id')
        room = Room.objects.get(id=room_id)
        message = Message.objects.create(creator=self.user, room=room, content=content)
        room.refresh_from_db()
        message_serialize = {**ChatRoomMessageSerialier(message).data}
        async_to_sync(self.channel_layer.group_send)(
            room.group_name,
            {
                "type": "chat_message",
                **message_serialize
            }
        )

    def chat_message(self, event):
        super().send(text_data=json.dumps(event, ensure_ascii=False))


class ChatAsyncConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.chat_rooms: Any = []

    async def connect(self):
        try:
            self.user = self.scope['user']
            self.chat_rooms = await database_sync_to_async(self.user.room_set.select_related().all)()
            await self.accept()
            await self.import_user_client()
            async for room in self.chat_rooms:
                await self.channel_layer.group_add(room.group_name, self.channel_name)
            await self.channel_layer.group_add("broadcast", self.channel_name)
        except:
            raise StopConsumer

    async def disconnect(self, code):
        async for room in self.chat_rooms:
            await self.channel_layer.group_discard(room.group_name, self.channel_name)
        await self.channel_layer.group_discard("broadcast", self.channel_name)
        await database_sync_to_async(Client.objects.filter(user=self.user).delete)()
        raise StopConsumer

    async def receive_json(self, content, **kwargs):
        room_id = content.get('room_id')
        content = content.get('content')
        await self.messaging(room_id, content)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event, ensure_ascii=False))

    @sync_to_async
    def room_serialize(self, room: Room):
        return RoomSerializer(room, context={'user': self.user.id}).data

    async def messaging(self, room_id: int, content: str) -> Dict[str, bool]:
        # import_message_to_db.delay(self.user.id, room_id, content)
        await database_sync_to_async(Message.objects.create)(room_id=room_id, content=content, creator=self.user)
        room = await database_sync_to_async(Room.objects.get)(id=room_id)
        data = await self.room_serialize(room)
        await self.send_message_to_group(room.group_name, data)
        return {"status": True}

    async def send_message_to_group(self, group_name, data):
        await self.channel_layer.group_send(
            group_name,
            {
                "type": "chat_message",
                **data
            }
        )
    async def import_user_client(self):
        await database_sync_to_async(Client.objects.filter(user=self.user).delete)()
        await database_sync_to_async(Client.objects.create)(user=self.user, channel_name=self.channel_name)
