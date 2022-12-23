from model_bakery.recipe import Recipe, foreign_key, related, seq
from market.models import *
from django.contrib.auth import get_user_model
from market.baker_recipes import *
from itertools import cycle

ip_14_pro_max_owner_huy = Recipe(Product, name='IPhone 14 Pro Max 512GB', sold_amount=10, description='abc',
                                 owner=foreign_key(user_huy))

units_product_option_ip_14_pro_max = ['Rose', 'Gold', 'Blue', 'White', 'Red']
product_option_ip_14_pro_max = Recipe(Option, unit_in_stock=50, price=2000000, unit=cycle(units_product_option_ip_14_pro_max),
                                      base_product=foreign_key(ip_14_pro_max_owner_huy))


order_huy_product_recipe = order.extend(customer=foreign_key(user_normal), store=foreign_key(user_huy))
order_detail_product_option_recipe = order_detail.extend(product_option=product_option_ip_14_pro_max.make,
                                            order=foreign_key(order_huy_product_recipe), _quantity=5)
