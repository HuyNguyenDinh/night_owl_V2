from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/user/connection/', consumers.UserConnectionConsumer.as_asgi()),
    path("ws/user/chatroom/<int:room_id>/", consumers.ChatConsumer.as_asgi())
]
