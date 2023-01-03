from tests.market.fixtures.entities.users import customer, user_has_address_instance
from tests.market.fixtures.entities.addresses import bh_address
from model_bakery.recipe import Recipe
from market.models import *
from typing import List
from tests.market.fixtures.usecases.scenarios.ver1 import *

# def customer_has_address(**kwargs) -> User | List[User]:
#     return user_has_address_instance(_address_recipe=bh_address, _customer_recipe=customer, **kwargs)
customer_fixture = Fixture(
    _instance=customer,
    _reverse_relationship_recipe={
        'address': ('creator', bh_address)
    }
)

customer_has_address = Bridge(
    _previous=None,
    _current=customer_fixture
)
