import time
from tests.market.fixtures.usecases.instance_results.buying import customer_has_address
from tests.market.test_models_new import ITestCase
from tests.market.fixtures.usecases.instance_results import *
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from market.models import *
from django.core.management import call_command
import sys

cloudinary_sameple_response = {
    "asset_id": "b5e6d2b39ba3e0869d67141ba7dba6cf",
    "public_id": "eneivicys42bq5f2jpn2",
    "version": 1570979139,
    "version_id": "98f52566f43d8e516a486958a45c1eb9",
    "signature": "abcdefghijklmnopqrstuvwxyz12345",
    "width": 1000,
    "height": 672,
    "format": "jpg",
    "resource_type": "image",
    "created_at": "2017-08-11T12:24:32Z",
    "tags": [],
    "pages": 1,
    "bytes": 350749,
    "type": "upload",
    "etag": "5297bd123ad4ddad723483c176e35f6e",
    "placeholder": False,
    "url": "http://res.cloudinary.com/demo/image/upload/v1570979139/eneivicys42bq5f2jpn2.jpg",
    "secure_url": "https://res.cloudinary.com/demo/image/upload/v1570979139/eneivicys42bq5f2jpn2.jpg",
    "access_mode": "public",
    "original_filename": "sample",
    "eager": [
        {"transformation": "c_pad,h_300,w_400",
         "width": 400,
         "height": 300,
         "url": "http://res.cloudinary.com/demo/image/upload/c_pad,h_300,w_400/v1570979139/eneivicys42bq5f2jpn2.jpg",
         "secure_url": "https://res.cloudinary.com/demo/image/upload/c_pad,h_300,w_400/v1570979139/eneivicys42bq5f2jpn2.jpg"},
        {"transformation": "c_crop,g_north,h_200,w_260",
         "width": 260,
         "height": 200,
         "url": "http://res.cloudinary.com/demo/image/upload/c_crop,g_north,h_200,w_260/v1570979139/eneivicys42bq5f2jpn2.jpg",
         "secure_url": "https://res.cloudinary.com/demo/image/upload/c_crop,g_north,h_200,w_260/v1570979139/eneivicys42bq5f2jpn2.jpg"}]
}

class IAPITestCase(ITestCase):
    client: APIClient

class IOrderViewSetTest(IAPITestCase):
    cart: CartDetail
    def create(self) -> None:
        print(self.cart)
        self.client.force_authenticate(user=self.cart.customer)
        data = {
            "list_cart": [
                self.cart.id
            ]
        }
        response = self.client.post(f"/market/orders/", data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class OrderViewSetTest(IOrderViewSetTest, APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = customer_has_address.bridge_extend().get_fixture()
        cls.cart = add_to_cart.valid_cart_detail.get_fixture()
    def setUp(self):
        super().setUp()
        print('setting up')

    def tearDown(self) -> None:
        print('tear down')
        print(User.objects.all())
        sysout = sys.stdout
        sys.stdout = open(f'./fixtures/market/views/OrderViewSet/{self._testMethodName}.json', 'w')
        call_command('dumpdata', 'market', indent=2)
        sys.stdout = sysout

    def test_create(self) -> None:
        print(User.objects.all())
        print("___end_create_____")
        self.create()
    def test_stop(self) -> None:
        print(User.objects.all())
        print("___________")
# class IProductViewSetTest(IAPITestCase):
#     def get(self) -> None:
#         temp_option = add_options.valid_product_option_full

