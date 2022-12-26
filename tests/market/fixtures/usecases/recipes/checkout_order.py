from tests.market.fixtures.usecases.recipes.add_to_cart import *
from tests.market.fixtures.usecases.recipes.add_options import *
from market.baker_recipes import *
from tests.market.fixtures.entities.orders import *
from tests.market.fixtures.entities.orderdetails import *

checkout_order_cod_valid = general_order_detail.make(
    order = checkout_order_cod.make(
        customer=customer_has_address,
        store=cart_detail.product_option.base_product.owner
    ),
    product_option=cart_detail.product_option,
    unit_price=cart_detail.product_option.price,
).order

checkout_order_momo_valid = general_order_detail.make(
    order = checkout_order_momo.make(
        customer=customer_has_address,
        store=cart_detail.product_option.base_product.owner
    ),
    product_option=cart_detail.product_option,
    unit_price=cart_detail.product_option.price,
).order

checkout_order_cod_point = general_order_detail.make(
    order = checkout_order_point.make(
        customer=customer_has_address,
        store=cart_detail.product_option.base_product.owner
    ),
    product_option=cart_detail.product_option,
    unit_price=cart_detail.product_option.price,
).order