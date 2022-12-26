from tests.market.fixtures.entities.valid_logic import *
from tests.market.fixtures.entities.users import *
from tests.market.fixtures.usecases.recipes import *
from tests.market.test_models_new import ITestCase
from django.test.testcases import TransactionTestCase
from django.test import override_settings
from rest_framework.test import APIClient
from rest_framework import status
from market.models import *
from market.baker_recipes import *
from unittest.mock import patch
import os

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
    api_client: APIClient

class IOrderViewSetTest(IAPITestCase):
    @override_settings(DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DB_NAME', 'test_night_owl'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
            'HOST': os.getenv('DB_HOST', "127.0.0.1"),
            'PORT': os.getenv('DB_PORT', 5432),
        }
    })
    def create(self) -> None:
        self.api_client.force_authenticate(user=self.users.get('customer'))
        data = {
            "list_cart": [
                add_to_cart.cart_detail.id
            ]
        }
        response = self.api_client.post(f"/market/orders/", data=data,format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class OrderViewSetTest(IOrderViewSetTest, TransactionTestCase):
    def setUp(self) -> None:
        self.users = {
            'customer': buying.customer_has_address,
            'business': selling.business_has_address,
        }
        self.api_client = APIClient()

    def test_create(self) -> None:
        self.create()

class IProductViewSetTest(IAPITestCase):
    def get(self) -> None:
        temp_option = add_options.valid_product_option_full

