from tests.market.fixtures.usecases.recipes.add_products import product_valid
from tests.market.fixtures.entities.options import *
from model_bakery.recipe import Recipe
from market.models import *
from typing import List

def valid_product_option_emtpy(**kwargs) -> Option:
    return product_option_instance(_product_option_recipe=product_option_empty, _product=product_valid(), **kwargs)
def multi_product_option_empty(_quantity: int = 2, **kwargs) -> List[Option]:
    return product_option_instances(_product_option_recipe=product_option_empty, _product=product_option_empty,
                                    _quantity=_quantity, **kwargs)
def valid_product_option_full(**kwargs) -> Option:
    return product_option_instance(_product_option_recipe=product_option_full, _product=product_valid(), **kwargs)
def multi_valid_product_option_full(_quantity: int = 2, **kwargs) -> List[Option]:
    return product_option_instances(_product_option_recipe=product_option_full, _product=product_valid(),
                                    _quantity=_quantity, **kwargs)
