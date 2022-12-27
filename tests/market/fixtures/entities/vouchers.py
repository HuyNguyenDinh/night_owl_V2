from market.baker_recipes import general_voucher
from market.models import *
from model_bakery.recipe import Recipe
from typing import List

def voucher_instance(_voucher_recipe: Recipe, _creator: User, _products: List[Product], **kwargs) -> Voucher | List[Voucher]:
    return _voucher_recipe.make(creator=_creator, products=_products, make_m2m=True, **kwargs)

percentage_voucher = general_voucher.extend(is_percentage=True)
not_percentage_voucher = general_voucher.extend(is_percentage=False)