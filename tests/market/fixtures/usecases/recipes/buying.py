from tests.market.fixtures.usecases.recipes.add_to_cart import *
from tests.market.fixtures.entities.users import customer
from tests.market.fixtures.entities.valid_logic import bh_address

customer_has_address = bh_address.make(creator=customer.make()).creator
