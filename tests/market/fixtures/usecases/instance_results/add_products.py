from tests.market.fixtures.usecases.instance_results.selling import business_has_address
from market.baker_recipes import *
from tests.market.fixtures.entities.products import *
from typing import List
from market.models import *

def product_valid(**kwargs) -> Product | List[Product]:
    return product_instance(general_product, _owner=business_has_address(), **kwargs)