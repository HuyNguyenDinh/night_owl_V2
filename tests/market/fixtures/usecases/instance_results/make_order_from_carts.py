from tests.market.fixtures.usecases.instance_results.add_to_cart import *
from tests.market.fixtures.entities.orders import *
from tests.market.fixtures.entities.cartdetail import *
from tests.market.fixtures.entities.users import *
from market.utils import make_order_from_list_cart

# order_fixture = Fixture(
#     _instance=Order.recipe()
# )
#
# order_from_cart_fixtures = order_fixture.set_instance(
#     _instance=make_order_from_list_cart(valid_cart_details.bridge_extend().get_fixture())
# )

# valid_uncheckout_order_from_carts = Bridge

# def valid_uncheckout_order_from_carts(_carts_quantity: int = 3) -> Order:
#     carts = multi_valid_cart_detail_of_product(_quantity=_carts_quantity)
#     list_cart_ids = [cart.id for cart in carts]
#     return make_order_from_list_cart(list_cart_ids, carts[0].customer.id, data={'list_cart': list_cart_ids})[0]
#
# def valid_uncheckout_orders_from_carts(_stores_quantity: int = 3, _carts_quantity_each_one: int = 3) -> List[Order]:
#     carts: List[CartDetail] = multi_valid_carts_of_customer()
#     list_cart_ids = [cart.id for cart in carts]
#     return make_order_from_list_cart(list_cart_ids, carts[0].customer.id, data={'list_cart': list_cart_ids})