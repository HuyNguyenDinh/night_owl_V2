from tests.market.fixtures.usecases.recipes.selling import business_has_address
from market.baker_recipes import *
from tests.market.fixtures.entities.products import *

product_valid = general_product.make(owner=business_has_address)
product_valid_recipe = general_product.extend(owner=business_has_address)