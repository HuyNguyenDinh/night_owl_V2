from django.test import TestCase
from market.models import *
from django.utils import timezone
from market.utils import *
from unittest.mock import patch
import json
from model_bakery import baker
from itertools import cycle
from market.baker_recipes import *
import unittest
from parameterized import parameterized
from django.core import mail
import pytz

utc = pytz.UTC
tzinfo = pytz.UTC
#
#
# class EmailTest(TestCase):
#     @parameterized.expand([
#         ('huyn27316@gmail.com', 'Subject a', 'Test a', 1),
#         ('huyn27317@gmail.com', 'Subject b', 'Test b', 1),
#         ('huyn27318@gmail.com', 'Subject c', 'Test c', 1),
#         ('huyn27319@gmail.com', 'Subject d', 'Test d', 1)
#     ])
#     def test_send_email(self, receiver, subject, content, expected):
#         send_email(receiver, subject, content)
#         self.assertEqual(len(mail.outbox), expected)
#         self.assertEqual(mail.outbox[0].subject, subject)
#
#
# class CheckNowInDatetimeRangeTest(unittest.TestCase):
#     @classmethod
#     def setUp(cls) -> None:
#
#         cls.start_date = timezone.datetime.now(tz=tzinfo) - timezone.timedelta(days=1)
#         cls.end_date = timezone.datetime.now(tz=tzinfo) + timezone.timedelta(days=1)
#
#     @parameterized.expand([
#         (timezone.datetime.now(tz=tzinfo) - timezone.timedelta(days=1),
#          timezone.datetime.now(tz=tzinfo) + timezone.timedelta(days=1), True),
#         (timezone.datetime.now(tz=tzinfo) - timezone.timedelta(days=2),
#          timezone.datetime.now(tz=tzinfo) + timezone.timedelta(days=2), True),
#         (timezone.datetime.now(tz=tzinfo) - timezone.timedelta(days=0),
#          timezone.datetime.now(tz=tzinfo) + timezone.timedelta(days=1), True),
#         (timezone.datetime.now(tz=tzinfo) + timezone.timedelta(days=1),
#          timezone.datetime.now(tz=tzinfo) + timezone.timedelta(days=1), False),
#     ])
#     def test_check_now_in_datetime_range(self, start_date, end_date, expected):
#         self.assertEqual(check_now_in_datetime_range(start_date, end_date), expected)
#
#
class ProductOrderOptionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        categories = ['Smartphone', 'Laptop', 'Clothes', 'Watch', 'Sneaker']
        cls.categories = baker.make(Category, _quantity=5, name=cycle(categories))
        cls.users = baker.make_recipe()

    # def setUp(self) -> None:
    #     categories = ['Smartphone', 'Laptop', 'Clothes', 'Watch', 'Sneaker']
    #     self.categories = baker.make(Category, _quantity=5, name=cycle(categories))
    #     self.users = [baker.make_recipe('market.user_huy'), baker.make_recipe('market.user_normal')]
    #     self.address = [huy_address.make(creator=self.users[0], note='abc'), user_normal_address.make(creator=self.users[1], note='abc')]
    #     self.product = product_ip_14_pro_max.make(owner=self.users[0], categories=self.categories, description='abc')
    #     unit = ['rose', 'gold', 'red']
    #     price = [30000000, 33000000, 31000000]
    #     self.product_options = product_option.make(_quantity=3, unit=cycle(unit), price=cycle(price), base_product=self.product)
    #     self.voucher = voucher.make(creator=self.users[0], products=[self.product])
    #     self.cart = cart.make(customer=self.users[1], product_option=self.product_options[0])
    #     self.order = baker.make(Order, customer=self.users[1], store=self.users[0], total_shipping_fee=25000)
    #     self.order_details = order_detail.make(_quantity=3, product_option=cycle(self.product_options),
    #                                            unit_price=cycle(price), order=self.order)
    #     self.bill = bill.make(order_payed=self.order, customer=self.users[1])

    def test_check_voucher_available(self):
        product_temp = self.product
        voucher_temp = self.voucher
        for option in Option.objects.all():
            if option.base_product.id == product_temp.id:
                self.assertEqual(check_voucher_available(option.id, voucher_temp.id), True)
            else:
                self.assertEqual(check_voucher_available(option.id, voucher_temp.id), False)

    @patch('market.utils.calculate_shipping_fee')
    def test_make_order_from_list_cart(self, cal_ship_mock):
        cal_ship_mock.return_value = json.dumps({
                        "code": 200,
                        "message": "Success",
                        "data": {
                            "total": 36300,
                            "service_fee": 36300,
                            "insurance_fee": 0,
                            "pick_station_fee": 0,
                            "coupon_value": 0,
                            "r2s_fee": 0
                        }
        })
        actual = make_order_from_list_cart(list_cart_id=[self.cart.id, ], user_id=self.users[1].id,
                                           data={"list_cart": [self.cart.id, ]})
#         expected = [Order.objects.last()]
#         self.assertEqual(actual, expected)
#
#     def test_check_discount_in_order(self):
#         actual = check_discount_in_order(self.order.orderdetail_set.all(), self.voucher.id)
#         expected = self.order.orderdetail_set.first().id
#         self.assertEqual(actual, expected)
#
#     def test_calculate_order_value_with_voucher(self):
#         actual = calculate_order_value_with_voucher(voucher=self.voucher, value=decimal.Decimal(1000000.0))
#         expected = decimal.Decimal(900000)
#         self.assertEqual(actual, expected)
#
#     def test_calculate_value(self):
#         total_price = sum([i.unit_price * i.quantity for i in self.order_details])
#         expected_with_voucher = round(total_price *
#                                       decimal.Decimal(0.9) + decimal.Decimal(self.order.total_shipping_fee), 2)
#         actual_with_voucher = calculate_value(self.order.id, voucher_id=self.voucher.id)
#         self.assertEqual(actual_with_voucher, expected_with_voucher)
#         expected_without_voucher = round(total_price + decimal.Decimal(self.order.total_shipping_fee), 2)
#         actual_without_voucher = calculate_value(self.order.id)
#         self.assertEqual(actual_without_voucher, expected_without_voucher)
#
#     def test_decrease_option_unit_instock(self):
#         actual: int = decrease_option_unit_instock(self.order_details[0].id).unit_in_stock
#         expected: int = 48
#         self.assertEqual(actual, expected)
#
#     def test_calculate_max_lwh(self):
#         actual = calculate_max_lwh(self.order.id)
#         expected = {'max_width': 1, 'max_height': 1, 'max_length': 1, 'total_weight': 3}
#         self.assertEqual(actual, expected)
#
#     def test_increase_unit_in_stock_when_cancel_order(self):
#         increase_unit_in_stock_when_cancel_order(self.order.id)
#         self.product_options[2].refresh_from_db()
#         actual = self.product_options[2].unit_in_stock
#         expected = 52
#         self.assertEqual(actual, expected)
#
#     @patch('market.utils.create_shipping_order')
#     def test_update_shipping_code(self, utils_mock):
#         utils_mock.return_value = json.dumps(
#             {
#                 "code": 200,
#                 "message": "Success",
#                 "data":
#                 {
#                     "order_code": "FFFNL9HH",
#                     "sort_code": "19-60-06",
#                     "trans_type": "truck",
#                     "ward_encode": "",
#                     "district_encode": "",
#                     "fee": {
#                         "main_service": 22000,
#                         "insurance": 11000,
#                         "station_do": 0,
#                         "station_pu": 0,
#                         "return": 0,
#                         "r2s": 0,
#                         "coupon": 0
#                     },
#                     "total_fee": "33000",
#                     "expected_delivery_time": "2020-06-03T16:00:00Z",
#                 },
#                 "message_display": "Tạo đơn hàng thành công. Mã đơn hàng: FFFNL9HH"
#             })
#         self.assertEqual(update_shipping_code(self.order.id), True)
