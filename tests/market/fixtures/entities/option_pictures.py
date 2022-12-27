from market.models import *
from model_bakery.recipe import Recipe
from typing import List

def option_with_picture_instance(_option_image_recipe: Recipe, _product_option: Option, **kwargs) -> Option | List[Option]:
    return _option_image_recipe.make(product_option=_product_option, **kwargs).product_option