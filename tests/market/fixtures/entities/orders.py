from market.baker_recipes import general_order
from model_bakery.recipe import Recipe
from market.models import *
from typing import List

# def order_instance(_order_detail_recipe: Recipe,
#                           _order_recipe: Recipe,
#                           _customer: User,
#                           _cart_id: CartDetail,
#                           **kwargs) -> Order:
#     return _order_detail_recipe.make(
#         order=_order_recipe.make(
#             customer=_customer,
#             store=_cart_id.product_option.base_product.owner
#         ),
#         product_option=_cart_id.product_option,
#         unit_price=_cart_id.product_option.price,
#         **kwargs
#     ).order


def order_instance(_order_recipe: Recipe,
                   _customer: User,
                   _store: User,
                   **kwargs) -> Order | List[Order]:
    return _order_recipe.make(customer=_customer, store=_store, **kwargs)


uncheckout_order = general_order.extend(status=0)
checkout_order_cod = general_order.extend(status=1)
checkout_order_momo = checkout_order_cod.extend(payment_type=1)
checkout_order_point = checkout_order_momo.extend(payment_type=2)

pending_order_cod = general_order.extend(status=2)
pending_order_momo = pending_order_cod.extend(payment_type=1)
pending_order_point = pending_order_momo.extend(payment_type=2)

complete_order_cod = general_order.extend(status=3)
complete_order_momo = complete_order_cod.extend(payment_type=1)
complete_order_point = complete_order_momo.extend(payment_type=2)

cancel_order_cod = general_order.extend(status=4)
cancel_order_momo = cancel_order_cod.extend(payment_type=1)
cancel_order_point = cancel_order_momo.extend(payment_type=2)