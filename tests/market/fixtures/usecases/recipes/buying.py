from tests.market.fixtures.usecases.recipes.add_to_cart import *
from tests.market.fixtures.models.base_recipes import *
from tests.market.fixtures.entities.users import customer
from tests.market.fixtures.entities.valid_logic import bh_address

customer_has_address = set_recipe_relationship(
    customer,
    address=bh_address
)
