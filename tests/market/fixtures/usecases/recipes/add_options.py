from tests.market.fixtures.usecases.recipes.add_products import product_valid
from tests.market.fixtures.recipe_setups import set_recipe_relationship
from tests.market.fixtures.entities.options import *

valid_product_option_emtpy = product_option_empty.make(base_product=product_valid)
valid_product_option_emtpy_recipe = product_option_empty.extend(base_product=product_valid)

valid_product_option_full = product_option_full.make(base_product=product_valid)
valid_product_option_full_recipe = product_option_full.extend(base_product=product_valid)

