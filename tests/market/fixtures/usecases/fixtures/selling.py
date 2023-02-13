from tests.market.fixtures.entities.addresses import q7_address
from tests.market.fixtures.entities.users import business
from tests.market.fixtures.usecases.scenarios.ver1 import Fixture

__all__ = [
    "business_has_address_ft"
]

business_has_address_ft = Fixture(
    _instance=business,
    _reverse_relationship_recipe={
        'address': ('creator', q7_address)
    }
)
