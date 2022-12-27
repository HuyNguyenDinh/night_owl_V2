from tests.market.fixtures.entities.users import customer, user_has_address_instance
from tests.market.fixtures.entities.valid_logic import bh_address
from model_bakery.recipe import Recipe
from market.models import *
from typing import List

def customer_has_address(**kwargs) -> User | List[User]:
    return user_has_address_instance(_address_recipe=bh_address, _customer_recipe=customer, **kwargs)
