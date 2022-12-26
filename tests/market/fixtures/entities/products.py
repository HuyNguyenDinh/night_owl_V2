from market.baker_recipes import general_product

available_product = general_product.extend(is_available=True)
not_available_product = general_product.extend(is_available=False)