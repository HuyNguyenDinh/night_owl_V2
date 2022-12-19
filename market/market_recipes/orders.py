from model_bakery.recipe import Recipe, foreign_key, related, seq
from market.models import *
from django.contrib.auth import get_user_model
from market.baker_recipes import *
from itertools import cycle

ip_14_pro_max_owner_huy = product_ip_14_pro_max.extend(owner=foreign_key(user_huy))
units_product_option_ip_14_pro_max = ['Rose', 'Gold', 'Blue', 'White', 'Red']
product_option_ip_14_pro_max = product_option.extend(base_product=foreign_key(ip_14_pro_max_owner_huy), price=2000000,
                                                     unit=cycle(units_product_option_ip_14_pro_max))
order_huy_product_recipe = Recipe(_model=Order, customer=foreign_key(user_normal), store=foreign_key(user_huy))
order_detail_product_option_recipe = order_detail.extend(product_option=product_option_ip_14_pro_max.make,
                                            order=foreign_key(order_huy_product_recipe), _quantity=5)
