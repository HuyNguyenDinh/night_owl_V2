from market.baker_recipes import general_bill
from model_bakery.recipe import Recipe
from market.models import *
from typing import List

def bill_instance(_bill_recipe: Recipe, _order_payed: Order, _customer: User, **kwargs) -> Bill | List[Bill]:
    return _bill_recipe.make(order_payed=_order_payed, customer=_customer, **kwargs)

payed_bill = general_bill.extend(payed=True)
not_payed_bill = general_bill.extend(payed=False)