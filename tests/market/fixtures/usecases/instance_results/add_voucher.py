from tests.market.fixtures.usecases.instance_results.add_products import *
from tests.market.fixtures.entities.vouchers import *

def valid_percentage_voucher_of_product(**kwargs) -> Voucher:
    return voucher_instance(_voucher_recipe=percentage_voucher,
                            _products=[product_valid()],
                            **kwargs)

def valid_percentage_voucher_of_products(_product_quantity: int = 3, **kwargs) -> Voucher:
    list_temp_products = [product_valid() for _ in range(_product_quantity)]
    return voucher_instance(_voucher_recipe=percentage_voucher,
                            _products=list_temp_products,
                            **kwargs)

def valid_not_percentage_voucher_of_product(**kwargs) -> Voucher:
    return voucher_instance(_voucher_recipe=not_percentage_voucher,
                            _products=[product_valid()],
                            **kwargs)

def valid_not_percentage_voucher_of_products(_product_quantity: int = 3, **kwargs) -> Voucher:
    list_temp_products = [product_valid() for _ in range(_product_quantity)]
    return voucher_instance(_voucher_recipe=not_percentage_voucher,
                            _products=list_temp_products,
                            **kwargs)
