from tests.market.fixtures.models.base_recipes import *
from model_bakery.recipe import foreign_key, seq, Recipe

__all__ = [
    "customer",
    "business",
    "business_product",
    "business_product_option"
]

customer = general_user.extend(email_verified=True, phone_verified=True)
business = general_user.extend(email_verified=True, phone_verified=True, is_business=True)
business_product = general_product.extend(owner=foreign_key(business))
business_product_option = general_product_option.extend(base_product=foreign_key(business_product))

__recipe__ = [
    customer,
    business,
    business_product,
    business_product_option
]