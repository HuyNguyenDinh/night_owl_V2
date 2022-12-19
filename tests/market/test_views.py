from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from market.models import *
import base64
import json
from unittest.mock import patch
from model_bakery import baker
from itertools import cycle
from market.baker_recipes import *
import numpy as np
from market.serializers import *
from market.paginations import *
from django.conf import settings
import os
from market.market_recipes.orders import *

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

class CategoryViewSetTest(APITestCase):
    def setUp(self) -> None:
        categories = ['Smartphone', 'Laptop', 'Clothes', 'Watch', 'Sneaker']
        self.categories = baker.make(Category, _quantity=5, name=cycle(categories))

    def test_get_list_categories(self):
        url = reverse('category-list')
        paginator = CategoryPagination()
        queryset = Category.objects.all()

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code,  status.HTTP_200_OK)

    def test_get_category_vouchers_available(self):
        response = self.client.get(f'/market/category/{self.categories[0].id}/vouchers-available/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = user_huy.make()
    def test_create_user(self):
        data = {
          "first_name": "Business",
          "last_name": "Normal",
          "email": "nightowl.business.normal@gmail.com",
          "phone_number": "84528649807",
          "password": "0937461321Huy@"
        }
        response = self.client.post(path=f'/market/users/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_current_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(path=f'/market/users/current-user/', format='json')
        self.assertEqual(response.data, UserSerializer(self.user).data)


class ProductViewSetTest(APITestCase):
    @patch('cloudinary.uploader.upload')
    def setUp(self, post_cloudinary_mock) -> None:
        ### Mock up the function that post the image to cloudinary when save an image to storage
        post_cloudinary_mock.return_value = cloudinary_sameple_response

        ### List category name
        categories = ['Smartphone', 'Laptop', 'Clothes', 'Watch', 'Sneaker']

        """
        Create the list contains Category Instance (Created and saved into Database) with amount define by _quantity
        use cycle() in itertool module as an iterator ordered
        """
        self.categories = baker.make(Category, _quantity=5, name=cycle(categories))
        ### Create list User Instance
        self.users: list[User] = [user_huy.make(), user_normal.make()]

        """
        List product name then create product for each product name with relationship "categories" (ManyToMany) and 
        "owner" (Foreign key)
        """
        product_name = ["IPhone", "Macbook"]
        self.products: list[Product] = product_ip_14_pro_max.make(_quantity=2, name=cycle(product_name), categories=self.categories,
                                                                  owner=self.users[0], description='abc')

        """
        List unit and price of product option as zip() function
        Then create a list that contains the list option of each product
        """
        unit = ['rose', 'gold', 'red']
        price = [30000000, 33000000, 31000000]
        self.options: list[list[Option]] = [
            product_option.make(base_product=self.products[0], _quantity=3, unit=cycle(unit), price=cycle(price)),
            product_option.make(base_product=self.products[1], _quantity=3, unit=cycle(unit), price=cycle(price))
        ]

        """
        Create rating for each product with relationship
        """

        ### Create 2 order with relationship
        self.order = order.make(_quantity=2, customer=self.users[1], store=self.users[0])

        ### Flat all option into an 1D array
        all_option = np.array(self.options).flatten()

        ### Get all price option in flat option array
        all_option_unit_price = [i.price for i in all_option]

        ### Define a Recipe extend from order_detail Recipe in baker_recipes.py
        order_detail_recipe_extend = order_detail.extend(product_option=cycle(all_option), unit_price=cycle(all_option_unit_price))
        self.order_details = order_detail_recipe_extend.make(order=cycle(self.order), _quantity=6)
        self.rating = rating.make(_quantity=2, creator=self.users[1], product=cycle(self.products))
        ### Create a Voucher Instance
        self.voucher = voucher.make(products=self.products, code='TEST')


    def test_list_products(self):
        url = reverse('products-list')

        ### Make request
        response = self.client.get(url, format='json')

        ### Assert response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('cloudinary.uploader.upload')
    def test_post_products(self, post_cloudinary_mock):
        ### Mock up the function that post the image to cloudinary when save an image to storage
        post_cloudinary_mock.return_value = cloudinary_sameple_response

        ### Authenticate Request
        self.client.force_authenticate(user=self.users[0])

        ### Make a base64 string from an image
        with open(os.path.abspath(f'%s/tests/test_img.jpeg' % settings.BASE_DIR), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

            ### make data dict as request payload
            data = {
                "name": "IPhone 11 Pro Max",
                "description": "Mo ta abc xyz",
                "categories": [i.id for i in self.categories],
                "image": encoded_string
            }

            ### encode data as json
            data_encode = json.dumps(data)
        response = self.client.post(f'/market/products/', data=data_encode, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_product_detail(self):
        response = self.client.get(f'/market/products/{self.products[0].id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('cloudinary.uploader.upload')
    def test_put_product(self, post_cloudinary_mock):
        post_cloudinary_mock.return_value = cloudinary_sameple_response
        self.client.force_authenticate(user=self.users[0])
        with open(os.path.abspath(f'%s/tests/test_img.jpeg' % settings.BASE_DIR), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            data = {
                "name": "IPhone 11 Pro Max",
                "description": "Chinh sua mo ta abc xyz",
                "categories": [i.id for i in self.categories],
                "image": encoded_string
            }
            data_encode = json.dumps(data)
        response = self.client.put(f'/market/products/{self.products[1].id}/', data=data_encode, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.delete(f'/market/products/{self.products[0].id}/', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_comments(self):
        response = self.client.get(f'/market/products/{self.products[0].id}/comments/', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_add_comment_without_buying_product(self):
        self.client.force_authenticate(user=self.users[0])
        data = {
            "rate": 4,
            "comment": "Test"
        }
        data_encode = json.dumps(data)
        response = self.client.post(f'/market/products/{self.products[0].id}/add-comment/', data=data_encode, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_add_comment_valid(self) -> None:
        self.client.force_authenticate(user=self.users[1])
        data = {
            "rate": 4,
            "comment": "Test"
        }
        data_encode = json.dumps(data)
        response = self.client.post(f'/market/products/{self.products[0].id}/add-comment/', data=data_encode,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('cloudinary.uploader.upload')
    def test_add_option(self, post_cloudinary_mock):
        post_cloudinary_mock.return_value = cloudinary_sameple_response
        self.client.force_authenticate(user=self.users[0])
        with open(os.path.abspath(f'%s/tests/test_img.jpeg' % settings.BASE_DIR), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            data = {
                "unit": "Blue",
                "price": 25000000,
                "uploaded_images": [encoded_string]
            }
            encoded_data = json.dumps(data)
        response = self.client.post(f'/market/products/{self.products[0].id}/add-option/', data=encoded_data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_options(self):
        response = self.client.get(f'/market/products/{self.products[0].id}/options/', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_products_statistic_in_year(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(f'/market/products/products-statistic-count-in-year/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_products_statistic_count_in_month(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(f'/market/products/products-statistic-count-in-month/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_statistic_in_month(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(f'/market/products/{self.products[0].id}/product-statistic-in-month/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_statistic_in_year(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(f'/market/products/{self.products[0].id}/product-statistic-in-year/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vouchers_available_of_product(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(f'/market/products/{self.products[0].id}/vouchers-available/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class OrderViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.order_details = order_detail_product_option_recipe.make()

    def test_get_order(self):
        self.assertEqual(self.order_details[0].order, Order.objects.last())

    def test_get_customer_order(self):
        self.assertEqual(self.order_details[0].order.store, User.objects.get(phone_number="0937461321"))
