from django.test import TestCase
from .models import *
from django.utils import timezone
from .utils import *
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework_simplejwt.tokens import RefreshToken
from django.test import Client


class check_now_in_datetime_range_test(TestCase):

    def setUp(self) -> None:
        self.start_date = timezone.now() - timezone.timedelta(days=1)
        self.end_date = timezone.now() + timezone.timedelta(days=1)

    def test_function(self) -> None:
        self.assertEqual(check_now_in_datetime_range(self.start_date, self.end_date), True)


class Product_Order_Option_test(TestCase):

    def setUp(self) -> None:
        self.categories = []
        self.categories.append(Category(name='Smartphone'))
        self.categories.append(Category(name='Laptop'))
        Category.objects.bulk_create(self.categories)
        self.users = []
        self.users.append(User(email="huyn27316@gmail.com", phone_number="0937461321", email_verified=True,
                               phone_verified=True, is_business=True))
        self.users.append(User(email="nightowl.usernormal.1@gmail.com", phone_number="84937461321", email_verified=True,
                               phone_verified=True))
        User.objects.bulk_create(self.users)
        self.address = []
        self.address.append(Address.objects.create(province_id=202, district_id=1449, ward_id="20709",
                                                   creator=self.users[0], street="Bùi Văn Ba",
                                                   full_address="Bùi Văn Ba, Phường Tân Thuận Đông, Quận 7, Hồ Chí Minh"))
        self.address.append(Address.objects.create(province_id=204, district_id=1536, ward_id="480126",
                                                   creator=self.users[1], street="67/13 Hoàng Minh Chánh",
                                                   full_address="67/13 Hoàng Minh Chánh, phường Hóa An, TP Biên Hòa, Đồng Nai"))
        self.products = []
        self.products.append(Product.objects.create(name='IPhone 14 Pro Max 512GB', owner=self.users[0]))
        self.products.append(Product.objects.create(name='IPhone 14 Pro Max 256GB', owner=self.users[0]))
        for product in self.products:
            product.categories.add(self.categories[0])
        self.options = []
        self.options.append(Option(unit='Gold', unit_in_stock='50', price=40000000, base_product=self.products[0], height=5, weight=5))
        self.options.append(Option(unit='Grey', unit_in_stock='50', price=40000000, base_product=self.products[0], width=6))
        self.options.append(Option(unit='Green', unit_in_stock='50', price=40000000, base_product=self.products[0], length=7))
        self.options.append(Option(unit='Blue', unit_in_stock='50', price=30000000, base_product=self.products[1], weight=8))
        self.options.append(Option(unit='Red', unit_in_stock='50', price=30000000, base_product=self.products[1], width=9))
        self.options.append(Option(unit='Rose Gold', unit_in_stock='50', price=30000000, base_product=self.products[1], height=10))
        self.options.append(Option(unit='Purple', unit_in_stock='50', price=30000000, base_product=self.products[1], length=9))
        Option.objects.bulk_create(self.options)
        self.vouchers = []
        self.vouchers.append(Voucher(code="Huy1", discount=decimal.Decimal(10), is_percentage=True, creator=self.users[0]))
        Voucher.objects.bulk_create(self.vouchers)
        self.vouchers[0].products.add(self.products[0])
        self.carts = []
        self.carts.append(CartDetail(quantity=2, customer=self.users[1], product_option=self.options[0]))
        self.carts.append(CartDetail(quantity=2, customer=self.users[1], product_option=self.options[3]))
        CartDetail.objects.bulk_create(self.carts)
        self.orders = []
        self.orders.append(Order(customer=self.users[1], store=self.users[0], voucher_apply=self.vouchers[0],
                                 total_shipping_fee=15000.0))
        self.orders.append(Order(customer=self.users[1], store=self.users[0]))
        Order.objects.bulk_create(self.orders)
        self.order_details = []
        self.order_details.append(OrderDetail(quantity=2, order=self.orders[0], product_option=self.options[0],
                                              unit_price=self.options[0].price))
        self.order_details.append(OrderDetail(quantity=2, order=self.orders[0], product_option=self.options[3],
                                              unit_price=self.options[3].price))
        self.order_details.append(OrderDetail(quantity=2, order=self.orders[1], product_option=self.options[3],
                                              unit_price=self.options[3].price))
        OrderDetail.objects.bulk_create(self.order_details)

    def test_check_voucher_available(self):
        for option in self.options:
            if option.base_product.id == self.products[0].id:
                self.assertEqual(check_voucher_available(option.id, self.vouchers[0].id), True)
            else:
                self.assertEqual(check_voucher_available(option.id, self.vouchers[0].id), False)

    def test_make_order_from_list_cart(self):
        actual = make_order_from_list_cart(list_cart_id=[self.carts[0].id, self.carts[1].id], user_id=self.users[1].id,
                                           data={"list_cart": [self.carts[0].id, self.carts[1].id]})
        expected = list(Order.objects.all()[2:])
        self.assertEqual(actual, expected)

    def test_check_discount_in_order(self):
        actual = check_discount_in_order(self.order_details, self.vouchers[0].id)
        print(actual)
        expected = self.order_details[2].id
        self.assertNotEqual(actual, expected)

    def test_calculate_order_value_with_voucher(self):
        actual = calculate_order_value_with_voucher(voucher=self.vouchers[0], value=decimal.Decimal(1000000.0))
        expected = decimal.Decimal(900000)
        self.assertEqual(actual, expected)

    def test_calculate_value(self):
        expected_with_voucher = round(((self.options[0].price * 2) + (self.options[3].price * 2)) * decimal.Decimal(0.9) + decimal.Decimal(15000), 2)
        actual_with_voucher = calculate_value(self.orders[0].id, voucher_id=self.vouchers[0].id)
        self.assertEqual(actual_with_voucher, expected_with_voucher)
        expected_without_voucher = round((self.options[0].price * 2) + (self.options[3].price * 2) + decimal.Decimal(15000), 2)
        actual_without_voucher = calculate_value(self.orders[0].id)
        self.assertEqual(actual_without_voucher, expected_without_voucher)

    def test_decrease_option_unit_instock(self):
        actual = decrease_option_unit_instock(self.order_details[0].id).unit_in_stock
        expected = 48
        self.assertEqual(actual, expected)

    def test_calculate_max_lwh(self):
        actual = calculate_max_lwh(self.orders[0].id)
        expected = {'max_width': 1, 'max_height': 5, 'max_length': 1, 'total_weight': 13}
        self.assertEqual(actual, expected)

    def test_increase_unit_in_stock_when_cancel_order(self):
        runner = increase_unit_in_stock_when_cancel_order(self.orders[0].id)
        actual = (self.options[0].unit_in_stock, self.options[3].unit_in_stock)
        expected = (52, 52)
        self.assertEqual(actual, expected)
