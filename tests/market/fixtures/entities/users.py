from market.baker_recipes import *
from market.models import *
from model_bakery.recipe import Recipe
from typing import List

__all__ = [
    "customer",
    "business",
    "user_has_address_instance"
]

customer = general_user.extend(email_verified=True, phone_verified=True)
business = general_user.extend(email_verified=True, phone_verified=True, is_business=True)

def user_has_address_instance(_address_recipe: Recipe,
                              _customer_recipe: Recipe,
                              **kwargs) -> User | List[User]:
    return _address_recipe.make(creator=_customer_recipe.make(**kwargs)).creator
