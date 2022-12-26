from market.baker_recipes import *

__all__ = [
    "customer",
    "business",
]

customer = general_user.extend(email_verified=True, phone_verified=True)
business = general_user.extend(email_verified=True, phone_verified=True, is_business=True)

__recipe__ = [
    customer,
    business,
]