from django.test.testcases import TestCase
from tests.market.fixtures.entities.users import *
from tests.market.fixtures.usecases.instance_results import *
from market.baker_recipes import *
from market.models import *
from abc import ABC
from django.db.utils import IntegrityError
from model_bakery.recipe import foreign_key

class ITestCase(ABC):
    def assertEqual(self, *args, **kwargs):
        pass
    def assertRaise(self, *args, **kwargs):
        pass

class IUserRecipeModelTest(ITestCase):
    def create_customer(self) -> None:
        temp_cus = customer.make()
        self.assertEqual(User.objects.last().is_business, False)
        self.assertEqual(temp_cus, User.objects.last())
    def create_business(self) -> None:
        temp_business = business.make()
        self.assertEqual(User.objects.last().is_business, True)
        self.assertEqual(temp_business, User.objects.last())

class UserRecipeModelTest(IUserRecipeModelTest, TestCase):
    def test_create_customer(self) -> None:
        self.create_customer()
    def test_create_business(self) -> None:
        self.create_business()

class IAddressRecipeModelTest(ITestCase):
    def create_general_address(self) -> None:
        temp_address = general_address.make()
        self.assertEqual(temp_address, Address.objects.last())

class AddressRecipeModelTest(IAddressRecipeModelTest, TestCase):
    def test_create_general_address(self) -> None:
        self.create_general_address()

class IReportRecipeModelTest(ITestCase):
    def create_report(self) -> None:
        temp_report = general_report.make()
        self.assertEqual(temp_report, Report.objects.last())

class ReportRecipeModelTest(IReportRecipeModelTest, TestCase):
    def test_create_report(self) -> None:
        self.create_report()

class IProductRecipeModelTest(ITestCase):
    def create_general_product(self) -> None:
        self.assertRaise(ValidationError, general_product.make)
    def create_business_product(self) -> None:
        temp_product = add_products.product_valid.bridge_extend().get_fixture()
        self.assertEqual(temp_product, Product.objects.all())
    def create_negative_sold_amount_product(self) -> None:
        temp_product = general_product.extend(owner=business)
        self.assertRaise(IntegrityError, temp_product.make, sold_amount=-1)

class ProductRecipeModelTest(IProductRecipeModelTest, TestCase):
    def test_create_general_product(self) -> None:
        self.create_general_product()
    def test_create_business_product(self) -> None:
        self.create_business_product()
    def test_create_negative_sold_amount_product(self) -> None:
        self.create_negative_sold_amount_product()

class IOptionRecipeModelTest(ITestCase):
    def create_general_option(self) -> None:
        self.assertRaise(ValidationError, general_product_option.make)
    def create_business_option(self) -> None:
        temp_option = general_product_option.extend(
            base_product=foreign_key(general_product.extend(
                owner=foreign_key(business)
            ))
        ).make()
        self.assertEqual(temp_option, Option.objects.last())

class OptionRecipeModelTest(IOptionRecipeModelTest, TestCase):
    def test_create_general_option(self):
        self.create_general_option()
    def test_create_business_option(self) -> None:
        self.create_business_option()

class ICartDetailRecipeModelTest(ITestCase):
    def create_general_cart(self) -> None:
        self.assertRaise(ValidationError, general_cart_detail.make)
    def create_valid_cart(self) -> None:
        temp_cart = add_to_cart.valid_cart_detail.bridge_extend().get_fixture()
        self.assertEqual(temp_cart, CartDetail.objects.all())

class CartDetailRecipeModel(ICartDetailRecipeModelTest,TestCase):
    def test_create_general_cart(self) -> None:
        self.create_general_cart()
    def test_create_valid_cart(self) -> None:
        self.create_valid_cart()

class IOrderRecipeModelTest(ITestCase):
    def create_general_order(self) -> None:
        self.assertRaise(ValidationError, general_order.make)

class OrderRecipeModelTest(IOrderRecipeModelTest, TestCase):
    def test_create_general_order(self) -> None:
        self.create_general_order()

class IOrderDetailRecipeModelTest(ITestCase):
    def create_general_order_detail(self) -> None:
        self.assertRaise(ValidationError, general_order_detail.make)

class OrderDetailRecipeModelTest(IOrderDetailRecipeModelTest, TestCase):
    def test_create_general_order_detail(self) -> None:
        self.create_general_order_detail()

class IBillRecipeModelTest(ITestCase):
    def create_general_bill(self) -> None:
        self.assertRaise(ValidationError, general_bill.make)

class BillRecipeModelTest(IBillRecipeModelTest, TestCase):
    def test_create_general_bill(self) -> None:
        self.create_general_bill()

class IVoucherRecipeModelTest(ITestCase):
    def create_percent_voucher(self) -> None:
        temp_voucher = general_voucher.make(is_percentage=True, discount=10)
        self.assertEqual(temp_voucher, Voucher.objects.last())
    def create_percent_voucher_gt_100(self) -> None:
        self.assertRaise(ValidationError, general_voucher.make, is_percentage=True, discount=200)
    def create_specific_value_voucher(self) -> None:
        temp_voucher = general_voucher.make(discount=10000)
        self.assertEqual(temp_voucher, Voucher.objects.last())

class VoucherRecipeModelTest(IVoucherRecipeModelTest, TestCase):
    def test_create_percent_voucher(self) -> None:
        self.create_percent_voucher()
    def test_create_percent_voucher_gt_100(self) -> None:
        self.create_percent_voucher_gt_100()
    def test_create_specific_value_voucher(self) -> None:
        self.create_specific_value_voucher()