from tests.market.fixtures.usecases.fixtures.buying import customer_has_address_ft
from tests.market.fixtures.usecases.scenarios.ver1 import Bridge

__all__ = [
    "customer_has_address"
]

customer_has_address = Bridge(
    _previous=None,
    _current=customer_has_address_ft
)

__bridge__ = [
    customer_has_address
]
