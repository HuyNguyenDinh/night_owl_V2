from tests.market.fixtures.usecases.instance_results.make_order_from_carts import *
from tests.market.fixtures.usecases.instance_results.add_options import *
from market.baker_recipes import *
from tests.market.fixtures.entities.orders import *
from tests.market.fixtures.entities.orderdetails import *
from market.utils import checkout_order
from tests.market.fixtures.usecases.scenarios.ver2 import Chain


# def checkout_order_cod_valid(**kwargs) -> Order:
#     checkout_order(valid_uncheckout_order_from_carts().id, )
# def checkout_orders_cod_valid(**kwargs) -> List[Order]
#
# def checkout_order_momo_valid(**kwargs):
#     return order_instance(checkout_order_momo, customer_has_address(), , **kwargs)
#
# def checkout_order_cod_point(**kwargs):
#     return order_instance(checkout_order_point, customer_has_address(), , **kwargs)

class CheckoutOrderChain(Chain):
    def prepare_previous(self):
        self.previous.append(AddToCartChain())
        self.previous.append(AddOptionChain())

    def prepare_fixtures(self):
        self.fixtures['uncheckout_order'] = Fixture(
            _instance=Order.recipe(status=0),
        )

        self.fixtures['checkout_order'] = Fixture(
            _instance=Order.recipe(status=1)
        )

        self.fixtures['checkout_order_momo'] = Fixture(
            _instance=Order.recipe(status=1, payment_type=1)
        )

        self.fixtures['checkout_order_point'] = Fixture(
            _instance=Order.recipe(status=1, payment_type=2)
        )

        self.fixtures['order_detail'] = Fixture(
            _instance=OrderDetail.recipe()
        )

    def prepare_bridges(self):
        self.bridges['checkout_order_cod_valid'] = Bridge(
            _current=self.get_fixture_by_name('checkout_order'),
            _previous={
                'customer': self.get_bridge_by_name('customer_has_address'),
                'store': self.get_bridge_by_name('business_has_address'),
            }
        )

        self.bridges['checkout_order_momo_valid'] = Bridge(
            _current=self.get_fixture_by_name('checkout_order_momo'),
            _previous={
                'customer': self.get_bridge_by_name('customer_has_address'),
                'store': self.get_bridge_by_name('business_has_address'),
            }
        )

        self.bridges['checkout_order_point_valid'] = Bridge(
            _current=self.get_fixture_by_name('checkout_order_point'),
            _previous={
                'customer': self.get_bridge_by_name('customer_has_address'),
                'store': self.get_bridge_by_name('business_has_address')
            }
        )

        self.bridges['checkout_order_cod_valid_odd'] = Bridge(
            _current=self.get_fixture_by_name('order_detail'),
            _previous={
                'order': self.get_bridge_by_name('checkout_order_cod_valid'),
                'product_option': self.get_bridge_by_name('valid_product_option_full')
            }
        )

        self.bridges['checkout_order_momo_valid_odd'] = Bridge(
            _current=self.get_fixture_by_name('order_detail'),
            _previous={
                'order': self.get_bridge_by_name('checkout_order_momo_valid'),
                'product_option': self.get_bridge_by_name('valid_product_option_full')
            }
        )

        self.bridges['checkout_order_point_valid'] = Bridge(
            _current=self.get_fixture_by_name('order_detail'),
            _previous={
                'order': self.get_bridge_by_name('checkout_order_point_valid'),
                'product_option': self.get_bridge_by_name('valid_product_option_full')
            }
        )
