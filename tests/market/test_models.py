# from model_bakery import baker
# from django.test import TestCase
# from market.baker_recipes import *
# from django.db.utils import IntegrityError
# from django.utils import timezone
# from tests.market.fixtures.models.base_recipes import *
# from tests.market.fixtures.entities.users import *
#
# class UserProductOrderData(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user_huy = user_huy.make()
#         cls.user_normal = user_normal.make()
#         cls.product = product_ip_14_pro_max.make(owner=cls.user_huy)
#         cls.product_option = product_option.make(base_product=cls.product)
#         cls.order = order.make(store=cls.user_huy, customer=cls.user_normal)
#
# class UserModelTest(TestCase):
#
#     def setUp(self) -> None:
#         self.user = baker.make_recipe('market.user_huy')
#
#     def test_user_created(self) -> None:
#         self.assertEqual(self.user, User.objects.last())
#
#     def test_create_user_with_email_exist(self) -> None:
#         self.assertRaises(IntegrityError, baker.make, _model=User, email=self.user.email)
#
#     def test_create_user_with_phone_exist(self) -> None:
#         self.assertRaises(IntegrityError, baker.make, _model=User, phone_number=self.user.phone_number)
#
# class AddressModelTest(TestCase):
#     def setUp(self) -> None:
#         self.address = baker.make_recipe('market.user_normal_address')
#
#     def test_address_created(self) -> None:
#         self.assertEqual(self.address, Address.objects.last())
#
# class ProductModelTest(TestCase):
#     def setUp(self) -> None:
#         self.user_huy = user_huy.make()
#         self.product = product_ip_14_pro_max.make(owner=self.user_huy)
#
#     def test_product_created(self) -> None:
#         self.assertEqual(self.product, Product.objects.last())
#
#     def test_add_product_by_customer(self) -> None:
#         user_normal_temp = user_normal.make()
#         self.assertRaises(ValidationError, product_ip_14_pro_max.make, owner=user_normal_temp)
#
#     def test_negative_sold_amount(self) -> None:
#         self.assertRaises(IntegrityError, product_ip_14_pro_max.make, owner=self.user_huy, sold_amount=-1)
#
# class OptionModelTest(TestCase):
#     def setUp(self) -> None:
#         self.user_huy = user_huy.make()
#         self.product = product_ip_14_pro_max.make(owner=self.user_huy)
#
#     def test_add_option_with_negative_price(self) -> None:
#         self.assertRaises(IntegrityError, product_option.make, base_product=self.product, price=-9)
#
#     def test_add_option_with_zero_width(self) -> None:
#         self.assertRaises(IntegrityError, product_option.make, base_product=self.product, width=0)
#
#     def test_add_option_with_zero_height(self) -> None:
#         self.assertRaises(IntegrityError, product_option.make, base_product=self.product, height=0)
#
#     def test_add_option_with_zero_length(self) -> None:
#         self.assertRaises(IntegrityError, product_option.make, base_product=self.product, length=0)
#
#     def test_add_option_with_zero_weight(self) -> None:
#         self.assertRaises(IntegrityError, product_option.make, base_product=self.product, weight=0)
#
# class ReportModelTest(TestCase):
#
#     def setUp(self) -> None:
#         self.user = user_huy.make()
#         self.report = baker.make(Report, _quantity=5, reporter=self.user, content="abc")
#
#     def test_report_created(self) -> None:
#         self.assertEqual(self.report, list(Report.objects.all()))
#
# class ReplyModelTest(TestCase):
#     def setUp(self) -> None:
#         self.report = baker.make(Report, content='abc')
#         self.reply = baker.make(Reply, report=self.report, content='abc')
#
#     def test_reply_created(self) -> None:
#         self.assertEqual(self.reply, Reply.objects.first())
#
# class CategoryModelTest(TestCase):
#     def setUp(self) -> None:
#         self.category = baker.make(Category, _quantity=5)
#
#     def test_category_created(self) -> None:
#         self.assertEqual(self.category, list(Category.objects.all().order_by('id')))
#
#     def test_create_same_category(self):
#         baker.make(Category, name='Conflict')
#         self.assertRaises(IntegrityError, baker.make, _model=Category, name='Conflict')
#
#
# class OrderModelTest(TestCase):
#     def setUp(self) -> None:
#         self.user_huy = user_huy.make()
#         self.user_normal = user_normal.make()
#
#     def test_store_same_customer_order(self) -> None:
#         self.assertRaises(ValidationError, order.make, customer=self.user_huy, store=self.user_huy)
#
#     def test_valid_order(self) -> None:
#         order_valid = order.make(customer=self.user_normal, store=self.user_huy)
#         self.assertEqual(order_valid, Order.objects.last())
#
#     def test_negative_shipping_fee(self) -> None:
#         self.assertRaises(IntegrityError, order.make, customer=self.user_normal, store=self.user_huy, total_shipping_fee=-2)
#
#
# class VoucherModelTest(TestCase):
#     def setUp(self) -> None:
#         self.user_huy = user_huy.make()
#         self.product = product_ip_14_pro_max.make(owner=self.user_huy)
#
#     def test_create_valid_voucher(self) -> None:
#         voucher_temp = voucher.make()
#         self.assertEqual(voucher_temp, Voucher.objects.last())
#
#     def test_create_voucher_end_date_before_start_date(self) -> None:
#         self.assertRaises(IntegrityError, voucher.make, end_date=timezone.now() - timezone.timedelta(days=1))
#
#     def test_create_voucher_same_code(self) -> None:
#         self.assertRaises(IntegrityError, voucher.make, _quantity=2, code='ABCXYZ')
#
#
# class RatingModelTest(UserProductOrderData):
#     def setUp(self) -> None:
#         self.order_detail = order_detail.make(product_option=self.product_option, order=self.order)
#
#     def test_create_valid_rating(self) -> None:
#         rating_temp = rating.make(creator=self.user_normal, product=self.product)
#         self.assertEqual(rating_temp, Rating.objects.last())
#
#     def test_create_rating_zero(self) -> None:
#         self.assertRaises(IntegrityError ,rating.make, creator=self.user_normal, product=self.product, rate=0)
#
#     def test_create_rating_negative(self) -> None:
#         self.assertRaises(IntegrityError, rating.make, creator=self.user_normal, product=self.product, rate=-1)
#
#     def test_create_rating_without_bought(self) -> None:
#         self.assertRaises(ValidationError, rating.make, creator=self.user_normal, product=product_ip_14_pro_max.make(owner=self.user_huy))
#
# class OrderDetailModelTest(UserProductOrderData):
#     def test_create_valid_order_detail(self) -> None:
#         orderdetail = order_detail.make(order=self.order, product_option=self.product_option)
#         self.assertEqual(orderdetail, OrderDetail.objects.last())
#
#     def test_create_order_with_zero_quantity(self) -> None:
#         self.assertRaises(IntegrityError, order_detail.make, order=self.order, quantity=0, product_option=self.product_option)
#
#     def test_create_order_with_negative_quantity(self) -> None:
#         self.assertRaises(IntegrityError, order_detail.make, order=self.order, quantity=-1, product_option=self.product_option)
#
#     def test_create_order_with_zero_unit_price(self) -> None:
#         self.assertRaises(IntegrityError, order_detail.make, order=self.order, unit_price=0, product_option=self.product_option)
#
#     def test_create_order_with_negative_unit_price(self) -> None:
#         self.assertRaises(IntegrityError, order_detail.make, order=self.order, unit_price=-1, product_option=self.product_option)
#
#
# class BillModelTest(UserProductOrderData):
#
#     def test_create_valid_bill(self) -> None:
#         bill_temp = bill.make(order_payed=self.order, customer=self.user_normal)
#         self.assertEqual(bill_temp, Bill.objects.last())
#
#     def test_create_bill_with_negative_value(self) -> None:
#         self.assertRaises(IntegrityError, bill.make, order_payed=self.order, customer=self.user_normal, value=-200000)
