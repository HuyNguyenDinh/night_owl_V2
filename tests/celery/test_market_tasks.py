from django.test import TestCase, override_settings
from night_owl_market.celery import app
from market.tasks import *
from market.baker_recipes import *
from model_bakery import baker
from market.models import *

class CeleryMarketTasksTest(TestCase):
    def setUp(self) -> None:
        self.users = [user_huy.make(), user_normal.make()]
        self.room = baker.make(Room, user=self.users, group_name='test1', room_type=1)


    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_send_email_task(self):
        self.assertTrue(import_message_to_db.delay(self.users[0].id, self.room.id, "Alo"))
