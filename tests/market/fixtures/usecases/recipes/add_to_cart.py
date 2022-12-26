from tests.market.fixtures.entities.cartdetail import *
from tests.market.fixtures.usecases.recipes.add_options import *
from tests.market.fixtures.usecases.recipes.buying import *
from market.baker_recipes import *

cart_detail = general_cart_detail.make(
    product_option=valid_product_option_full,
    customer=customer_has_address
)

cart_detail_recipe = general_cart_detail.extend(
    product_option=valid_product_option_full,
    customer=customer_has_address
)
