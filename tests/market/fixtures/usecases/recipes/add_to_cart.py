from tests.market.fixtures.entities.cartdetail import *
from tests.market.fixtures.recipe_setups import set_recipe_relationship
from tests.market.fixtures.usecases.recipes.add_options import *

cart_detail = set_recipe_relationship(
    general_cart_detail,
    product_option=product_option_full
)
