from market.baker_recipes import general_order_detail
from market.models import *
from model_bakery.recipe import Recipe
from typing import List
from itertools import cycle

def order_detail_instance(_order_detail_recipe: Recipe,
                          _order: Order,
                          _product_option: Option,
                          **kwargs) -> OrderDetail:
    return _order_detail_recipe.make(order=_order, product_option=_product_option, **kwargs)
