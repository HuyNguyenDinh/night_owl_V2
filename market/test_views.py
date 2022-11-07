from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from market.models import *
import base64
import json
from unittest.mock import patch
from PIL import Image
from django.core.files import File


class CategoryViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.categories: list[Category] = []
        self.categories.append(Category(name='Smartphone'))
        self.categories.append(Category(name='Laptop'))
        Category.objects.bulk_create(self.categories)

    def test_get_list_categories(self):
        url = reverse('category-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code,  status.HTTP_200_OK)

    def test_get_category_vouchers_available(self):
        response = self.client.get(f'/market/category/{self.categories[0].id}/vouchers-available/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserViewSet(APITestCase):
    def test_create_user(self):
        data = {
          "first_name": "Business",
          "last_name": "Normal",
          "email": "nightowl.business.normal@gmail.com",
          "phone_number": "84528649807",
          "password": "0937461321Huy@"
        }
        response = self.client.post(path=f'/market/users/', data=data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProductViewSetTest(APITestCase):
    @patch('cloudinary.uploader.upload')
    def setUp(self, post_cloudinary_mock) -> None:
        post_cloudinary_mock.return_value = {
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
        self.categories: list[Category] = []
        self.categories.append(Category(name='Smartphone'))
        self.categories.append(Category(name='Laptop'))
        Category.objects.bulk_create(self.categories)
        self.users: list[User] = []
        self.users.append(User(email="huyn27316@gmail.com", phone_number="0937461321", email_verified=True,
                               phone_verified=True, is_business=True))
        self.users[0].set_password("0937461321Huy@")
        self.users.append(User(email="nightowl.usernormal.1@gmail.com", phone_number="84937461321", email_verified=True,
                               phone_verified=True))
        self.users[1].set_password("0937461321Huy@")
        User.objects.bulk_create(self.users)
        self.products: list[Product] = []
        image = File(open("/home/dinhhuy2005/Downloads/test_img.jpeg", mode="rb"), name='test_image')
        self.products.append(Product(name="test_product_1", description="ABC XYZ", picture=image, owner=self.users[0]))
        self.products.append(Product(name="test_product_2", description="ABC XYZ", picture=image, owner=self.users[1]))
        Product.objects.bulk_create(self.products)
        print(self.products)
        self.products[0].categories.add(*self.categories)
        self.products[1].categories.add(*self.categories)
        self.options: list[Option] = []
        self.options.append(Option(unit_in_stock=30, unit="Xanh", price=30000000, base_product=self.products[0]))
        self.options.append(Option(unit_in_stock=30, unit="Đỏ", price=31000000, base_product=self.products[1]))
        Option.objects.bulk_create(self.options)

    def test_list_products(self):
        url = reverse('products-list')
        response = self.client.get(url, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('cloudinary.uploader.upload')
    def test_post_products(self, post_cloudinary_mock):
        post_cloudinary_mock.return_value = {
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
            { "transformation": "c_pad,h_300,w_400",
              "width": 400,
              "height": 300,
              "url": "http://res.cloudinary.com/demo/image/upload/c_pad,h_300,w_400/v1570979139/eneivicys42bq5f2jpn2.jpg",
              "secure_url": "https://res.cloudinary.com/demo/image/upload/c_pad,h_300,w_400/v1570979139/eneivicys42bq5f2jpn2.jpg" },
            { "transformation": "c_crop,g_north,h_200,w_260",
              "width": 260,
              "height": 200,
              "url": "http://res.cloudinary.com/demo/image/upload/c_crop,g_north,h_200,w_260/v1570979139/eneivicys42bq5f2jpn2.jpg",
              "secure_url": "https://res.cloudinary.com/demo/image/upload/c_crop,g_north,h_200,w_260/v1570979139/eneivicys42bq5f2jpn2.jpg" }]
        }
        self.client.force_authenticate(user=self.users[0])
        with open("/home/dinhhuy2005/Downloads/test_img.jpeg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            data = {
                "name": "IPhone 11 Pro Max",
                "description": "Mo ta abc xyz",
                "categories": [self.categories[0].id, self.categories[1].id],
                "image": encoded_string
            }
            data_encode = json.dumps(data)
        response = self.client.post(f'/market/products/', data=data_encode, content_type='application/json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_product_detail(self):
        response = self.client.get(f'/market/products/{self.products[0].id}/')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_product(self):
        pass

