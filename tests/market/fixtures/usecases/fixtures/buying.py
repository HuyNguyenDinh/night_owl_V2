from tests.market.fixtures.usecases.scenarios.ver1 import Fixture
from tests.market.fixtures.entities.users import customer
from tests.market.fixtures.entities.addresses import bh_address

__all__ = [
    "customer_has_address_ft"
]

customer_has_address_ft = Fixture(
    _name="customer_has_address",
    _instance=customer,
    _reverse_relationship_recipe={
        'address': ('creator', bh_address)
    }
)
