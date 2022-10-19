from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/user/connection/', consumers.UserInboxConsumer.as_asgi()),
    re_path(r'ws/user/chat/', consumers.ChatConsumer.as_asgi())
]
