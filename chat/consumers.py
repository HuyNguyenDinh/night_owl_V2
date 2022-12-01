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


class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.room = None

    def connect(self):
        try:
            self.user = self.scope['user']
            room_id = self.scope["url_route"]["kwargs"]["room_id"]
            self.room = Room.objects.select_related().get(pk=room_id, user=self.user)
            self.accept()
            async_to_sync(self.channel_layer.group_add)(
                self.room.group_name,
                self.channel_name
            )
        except:
            raise StopConsumer

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room.group_name,
            self.channel_name
        )
        raise StopConsumer

    def receive_json(self, content, **kwargs):
        content = content.get('content')
        message = Message.objects.create(creator=self.user, room=self.room, content=content)
        self.room.refresh_from_db()
        message_serialize = {**ChatRoomMessageSerialier(message).data}
        async_to_sync(self.channel_layer.group_send)(
            self.room.group_name,
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
        self.chat_rooms = []

    async def connect(self):
        try:
            self.user = self.scope['user']
            print(self.user.id)
            self.chat_rooms = await database_sync_to_async(self.user.room_set.select_related().all)()
            await self.accept()
            await self.import_user_client()
            async for room in self.chat_rooms:
                await self.channel_layer.group_add(room.group_name, self.channel_name)
            await self.channel_layer.group_add("broadcast", self.channel_name)
            print(self.channel_name)
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
    def get_room_serializer(self, room):
        return RoomSerializer(room).data

    @sync_to_async
    def messaging(self, room_id: int, content: str) -> Dict[str, bool]:
        import_message_to_db.delay(self.user.id, room_id, content)
        return {"status": True}

    async def import_user_client(self):
        await database_sync_to_async(Client.objects.filter(user=self.user).delete)()
        await database_sync_to_async(Client.objects.create)(user=self.user, channel_name=self.channel_name)
