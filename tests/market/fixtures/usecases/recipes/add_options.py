from tests.market.fixtures.usecases.recipes.add_products import product_valid
from tests.market.fixtures.recipe_setups import set_recipe_relationship
from tests.market.fixtures.entities.options import *

valid_product_option_emtpy = set_recipe_relationship(
    product_option_empty,
    base_product=product_valid,
)

valid_product_option_full = set_recipe_relationship(
    product_option_full,
    base_product=product_valid
)

