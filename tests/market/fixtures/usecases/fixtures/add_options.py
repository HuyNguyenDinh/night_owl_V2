from tests.market.fixtures.usecases.scenarios.ver1 import Fixture
from tests.market.fixtures.entities.options import product_option_empty, product_option_full
from market.baker_recipes import general_product_option_picture

__all__ = [
    "option_empty_ft",
    "option_full_ft",
    "option_full_picture_fixture",
]

option_empty_ft = Fixture(_instance=product_option_empty)
option_full_ft = Fixture(_instance=product_option_full)
option_full_picture_fixture = Fixture(
    _instance=product_option_full,
    _reverse_relationship_recipe={
        'picture': ('product_option', general_product_option_picture)
    }
)

__fixtures__ = [
    option_empty_ft,
    option_full_ft,
    option_full_picture_fixture
]
