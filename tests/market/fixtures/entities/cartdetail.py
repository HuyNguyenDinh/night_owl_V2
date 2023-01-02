from market.baker_recipes import general_cart_detail
from model_bakery.recipe import Recipe
from market.models import *
from typing import List
from itertools import cycle

def cart_detail_instance(_cart_detail_recipe: Recipe,
                         _product_option: Option,
                         _customer: User,
                         **kwargs) -> CartDetail:
    return _cart_detail_recipe.make(
        product_option=_product_option,
        customer=_customer,
        **kwargs
    )

def cart_detail_instances(_cart_detail_recipe: Recipe,
                          _product_option: List[Option],
                          _customer: User,
                          **kwargs) -> List[CartDetail]:
    return _cart_detail_recipe.make(
        _quantity=len(_product_option),
        product_option=cycle(_product_option),
        customer=_customer,
        **kwargs
    )
