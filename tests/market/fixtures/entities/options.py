from market.baker_recipes import general_product_option
from django.db.models.fields import BigIntegerField
from model_bakery.recipe import Recipe
from market.models import *
from typing import List

def product_option_instance(_product_option_recipe: Recipe, _product: Product, **kwargs) -> Option | List[Option]:
    return _product_option_recipe.make(base_product=_product, **kwargs)


product_option_empty = general_product_option.extend(unit_in_stock=0)
product_option_full = general_product_option.extend(unit_in_stock=BigIntegerField.MAX_BIGINT)