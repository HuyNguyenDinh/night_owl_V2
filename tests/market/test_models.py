from market.models import *
from model_bakery import baker
from django.test import TestCase
from market.baker_recipes import *
from django.db.utils import IntegrityError


class UserModelTest(TestCase):

    def setUp(self) -> None:
        self.user = baker.make_recipe('market.user_huy')

    def test_user_created(self) -> None:
        self.assertEqual(self.user, User.objects.first())

    def test_create_user_with_email_exist(self) -> None:
        self.assertRaises(IntegrityError, baker.make, _model=User, email=self.user.email)

    def test_create_user_with_phone_exist(self) -> None:
        self.assertRaises(IntegrityError, baker.make, _model=User, phone_number=self.user.phone_number)


class AddressModelTest(TestCase):
    def setUp(self) -> None:
        self.address = baker.make_recipe('market.user_normal_address')

    def test_address_created(self) -> None:
        self.assertEqual(self.address, Address.objects.last())


class ProductModelTest(TestCase):
    def setUp(self) -> None:
        self.user = user_huy.make()
        self.product = product.make(owner=self.user)

    def test_product_created(self) -> None:
        self.assertEqual(self.product, Product.objects.last())


class CartDetailModelTest(TestCase):
    def setUp(self) -> None:
        self.user_huy = user_huy.make()
        self.product = product.make(owner=self.user_huy)
        self.product_option = product_option.make(base_product=self.product, unit="a", price=20000)

    def test_add_store_product_to_store_cart(self):
        self.assertRaises(ValidationError, baker.make, _model=CartDetail, customer=self.user_huy, product_option=self.product_option)

    def test_add_product_valid(self):
        cart_detail = cart.make(customer=user_normal.make())
        self.assertEqual(cart_detail, CartDetail.objects.last())

    def test_add_negative_quantity(self):
        self.assertRaises(IntegrityError, baker.make, _model=CartDetail, quantity=-2)


class ReportModelTest(TestCase):

    def setUp(self) -> None:
        self.user = user_huy.make()
        self.report = baker.make(Report, _quantity=5, reporter=self.user)

    def test_report_created(self) -> None:
        self.assertEqual(self.report, list(Report.objects.all()))


class ReplyModelTest(TestCase):
    def setUp(self) -> None:
        self.report = baker.make(Report)
        self.reply = baker.make(Reply, report=self.report)

    def test_reply_created(self) -> None:
        self.assertEqual(self.reply, Reply.objects.first())


class CategoryModelTest(TestCase):
    def setUp(self) -> None:
        self.category = baker.make(Category, _quantity=5)

    def test_category_created(self) -> None:
        self.assertEqual(self.category, list(Category.objects.all()))


class OrderModelTest(TestCase):
    def setUp(self) -> None:
        self.user_huy = user_huy.make()
        self.user_normal = user_normal.make()

    def test_invalid_order(self) -> None:
        self.assertRaises(ValidationError, order.make, customer=self.user_huy, store=self.user_huy)

    def test_valid_order(self) -> None:
        order_valid = order.make(customer=self.user_normal, store=self.user_huy)
        self.assertEqual(order_valid, Order.objects.last())

