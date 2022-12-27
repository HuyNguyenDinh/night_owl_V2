from tests.market.fixtures.usecases.recipes.make_order_from_carts import *
from tests.market.fixtures.usecases.recipes.add_options import *
from market.baker_recipes import *
from tests.market.fixtures.entities.orders import *
from tests.market.fixtures.entities.orderdetails import *


# def checkout_order_cod_valid(**kwargs) -> Order | List[Order]:
#     valid_uncheckout_order_from_carts()
#
# def checkout_order_momo_valid(**kwargs):
#     return order_instance(checkout_order_momo, customer_has_address(), , **kwargs)
#
# def checkout_order_cod_point(**kwargs):
#     return order_instance(checkout_order_point, customer_has_address(), , **kwargs)