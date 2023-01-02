from tests.market.fixtures.usecases.instance_results.add_products import product_valid
from tests.market.fixtures.usecases.instance_results.add_voucher import *
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

def product_percentage_voucher_option_emtpy(**kwargs) -> Option:
    temp_product = valid_percentage_voucher_of_product().products.first()
    return product_option_instance(_product_option_recipe=product_option_empty, _product=temp_product, **kwargs)

def multi_product_percentage_voucher_option_emtpy(_quantity: int = 3, **kwargs) -> List[Option]:
    temp_product = valid_percentage_voucher_of_product().products.first()
    return product_option_instances(_quantity=_quantity,
                                   _product_option_recipe=product_option_empty,
                                   _product=temp_product,
                                   **kwargs)

def product_percentage_voucher_option_full(**kwargs) -> Option:
    temp_product = valid_not_percentage_voucher_of_product().products.first()
    return product_option_instance(_product_option_recipe=product_option_full, _product=temp_product, **kwargs)

def multi_product_percentage_voucher_option_full(_quantity: int = 3, **kwargs) -> List[Option]:
    temp_product = valid_not_percentage_voucher_of_product().products.first()
    return product_option_instances(_product_option_recipe=product_option_full,
                                    _product=temp_product,
                                    _quantity=_quantity,
                                    **kwargs)

def multi_products_percentage_voucher_option_empty(_product_quantity: int = 3, **kwargs) -> List[List[Option]]:
    temp_products = list(valid_percentage_voucher_of_products().products.all())
    result: List[List[Option]] = []
    for p in temp_products:
        result.append(product_option_instances(_product_option_recipe=product_option_empty,
                                 _product=p,
                                 _quantity=_product_quantity,
                                 **kwargs))
