from django.core.mail import send_mail
from night_owl_market import settings
from .models import *
from chat.models import *
from chat.tasks import *
from market.serializers import *
from night_owl_market.celery import app
import asyncio
from typing import Any
from market.utils import make_order_from_list_cart
import json
from market.utils import calculate_shipping_fee
from django.db import transaction

@app.task()
def send_email_task(reciever: str, subject: str, content: str) -> None:
    to = [reciever]
    send_subject = subject
    send_content = content
    return send_mail(send_subject, send_content, settings.EMAIL_HOST_USER, to, False)


@app.task()
def import_message_to_db(user_id: int, room_id: int, content: str):
    user = get_user_model().objects.get(pk=user_id)
    room = Room.objects.get(pk=room_id)
    message = Message.objects.create(creator=user, room=room, content=content)
    room_serializer = RoomSerializer(room).data
    app.send_task('chat.tasks.create_message', args=(room_serializer, room.group_name))
    return {"status": True}


@app.task()
def call_api_shipping_fee_task(order_id: int):
    shipping_data = json.loads(calculate_shipping_fee(order_id=order_id))
    if shipping_data.get('code') == 200:
        try:
            with transaction.atomic():
                order = Order.objects.select_for_update().get(pk=1)
                shipping_fee = shipping_data.get('data').get('total')
                order.total_shipping_fee = shipping_fee
                order.save()
                order.refresh_from_db()
        except:
            return False
        else:
            return True
    return False
