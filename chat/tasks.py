from celery import shared_task
from django.core.mail import send_mail
from night_owl_market import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import *
from market.serializers import *
from night_owl_market.celery import app
import asyncio
from typing import Dict, Any


async def send_message_to_group(room: dict[str, str], group_name: str):
    channel_layer = get_channel_layer()
    print(channel_layer)
    await channel_layer.group_send(
        group_name,
        {
            "type": "chat_message",
            **room
        }
    )


async def send_message_to_channel(channel_name: str, content: Dict[str, Any]):
    channel_layer = get_channel_layer()
    print(channel_layer)
    await channel_layer.send(
        channel_name,
        {
            "type": "chat_message",
            **content
        }
    )


@app.task()
def create_message(room: dict[str, str], group_name: str):
    try:
        loop = asyncio.get_event_loop()
        print('got loop')
    except:
        loop = asyncio.new_event_loop()
        print('created loop')
    finally:
        loop.run_until_complete(send_message_to_group(room, group_name))
        return {"status": True}


@app.task()
def send_message_to_channel(channel_name: str, content: Dict[str, Any]):
    try:
        loop = asyncio.get_event_loop()
        print('got loop')
    except:
        loop = asyncio.new_event_loop()
        print('created loop')
    finally:
        loop.run_until_complete(send_message_to_channel(channel_name, content))
        return {"status": True}
