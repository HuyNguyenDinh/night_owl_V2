from market.baker_recipes import general_product
from market.models import *
from model_bakery.recipe import Recipe
from typing import List
def product_instance(_product_recipe: Recipe, _owner: User, **kwargs) -> Product | List[Product]:
    return _product_recipe.make(owner=_owner, **kwargs)

available_product = general_product.extend(is_available=True)
not_available_product = general_product.extend(is_available=False)