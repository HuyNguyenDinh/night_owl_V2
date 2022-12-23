from tests.market.fixtures.usecases.recipes.selling import business_has_address
from tests.market.fixtures.recipe_setups import set_recipe_relationship
from tests.market.fixtures.entities.products import *

product_valid = set_recipe_relationship(
    general_product,
    owner=business_has_address
)