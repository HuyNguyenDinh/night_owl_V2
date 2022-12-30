from tests.market.fixtures.usecases.instance_results.make_order_from_carts import *
from tests.market.fixtures.usecases.instance_results.add_options import *
from market.baker_recipes import *
from tests.market.fixtures.entities.orders import *
from tests.market.fixtures.entities.orderdetails import *
from market.utils import checkout_order


# def checkout_order_cod_valid(**kwargs) -> Order:
#     checkout_order(valid_uncheckout_order_from_carts().id, )
# def checkout_orders_cod_valid(**kwargs) -> List[Order]
#
# def checkout_order_momo_valid(**kwargs):
#     return order_instance(checkout_order_momo, customer_has_address(), , **kwargs)
#
# def checkout_order_cod_point(**kwargs):
#     return order_instance(checkout_order_point, customer_has_address(), , **kwargs)