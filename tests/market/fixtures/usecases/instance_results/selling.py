from tests.market.fixtures.usecases.instance_results.buying import user_has_address_instance
from tests.market.fixtures.entities.users import *
from tests.market.fixtures.entities.addresses import *
from model_bakery.recipe import Recipe
from market.models import *
from typing import List

def business_has_address(**kwargs) -> User | List[User]:
    return user_has_address_instance(_address_recipe=q7_address, _customer_recipe=business, **kwargs)
