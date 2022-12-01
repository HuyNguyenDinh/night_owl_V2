from django.urls import re_path

from chat import consumers

websocket_urlpatterns = [
    re_path(r'ws/user/connection/', consumers.ChatAsyncConsumer.as_asgi())
]
