from django.test import TestCase
from chat.consumers import *
from night_owl_market.asgi import application
from market.baker_recipes import *
from channels.testing import WebsocketCommunicator
from model_bakery import baker
from rest_framework_simplejwt.tokens import RefreshToken
import asyncio
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
import json
from channels.layers import get_channel_layer

class TestChatAsyncConsumer(APITestCase):

    @patch('night_owl_market.channels_middleware.get_user')
    def setUp(self, get_user_mock) -> None:
        self.users = [user_huy.make(), user_normal.make()]
        get_user_mock.return_value = self.users[0]
        self.room = baker.make(Room, user=self.users, group_name="test1", room_type=1)
        self.token = str(RefreshToken.for_user(self.users[0]).access_token)
        self.communicator = WebsocketCommunicator(application, f"/ws/user/connection/?token={self.token}")
        loop = asyncio.get_event_loop()
        self.connected, subprotocol = loop.run_until_complete(self.communicator.connect(timeout=5))
        self.communicator.scope['user'] = self.users[0]

    def test_connect_ws(self):
        self.assertTrue(self.connected)

    def tearDown(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.communicator.disconnect())

    # def test_send_ws(self):
    #     loop = asyncio.get_event_loop()
    #     message = {"type": "websocket.receive", "text": "hello"}
    #     channel_layer = get_channel_layer()
    #     loop.run_until_complete(channel_layer.group_send("chat", message))
    #     response = loop.run_until_complete(self.communicator.receive_from(timeout=5))
    #     self.assertEqual(response, "hello")

    def test_get_current_user(self):
        self.client.force_authenticate(self.users[0])
        resp = self.client.get(f'/market/users/current-user/', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

