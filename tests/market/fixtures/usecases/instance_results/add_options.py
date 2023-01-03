from tests.market.fixtures.usecases.instance_results.add_products import *
from tests.market.fixtures.usecases.instance_results.add_voucher import *
from tests.market.fixtures.entities.options import *
from model_bakery.recipe import Recipe
from market.models import *
from typing import List
from tests.market.fixtures.usecases.scenarios.ver1 import *

option_empty_fixture = Fixture(_instance=product_option_empty)
option_full_fixture = Fixture(_instance=product_option_full)
option_full_picture_fixture = Fixture(
    _instance=product_option_full,
    _reverse_relationship_recipe={
        'picture': ('product_option', general_product_option_picture)
    }
)

### Return product
valid_product_option_full = Bridge(
    _previous={
        'base_product': product_valid
    },
    _current=option_full_fixture
)

### Return [product1, product2, ...]
multi_valid_product_options_full = valid_product_option_full.bridge_extend(
    _current=option_empty_fixture.fixture_extend(
        _recipe_params={
            '_quantity': 3
        }
    )
)

multi_valid_product_voucher_options_full = multi_valid_product_options_full.bridge_extend(
    _previous={
        'base_product': product_percentage_valid
    }
)
