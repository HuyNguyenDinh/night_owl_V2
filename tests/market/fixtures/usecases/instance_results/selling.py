from tests.market.fixtures.usecases.instance_results.buying import user_has_address_instance
from tests.market.fixtures.entities.users import *
from tests.market.fixtures.entities.addresses import *
from model_bakery.recipe import Recipe
from market.models import *
from typing import List
from tests.market.fixtures.usecases.scenarios.ver1 import *

business_fixture = Fixture(
    _instance=business,
    _reverse_relationship_recipe={
        'address': ('creator', q7_address)
    }
)

business_has_address = Bridge(
    _previous=None,
    _current=business_fixture
)
