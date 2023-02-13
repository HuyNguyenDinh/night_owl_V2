from tests.market.fixtures.usecases.fixtures.selling import business_has_address_ft
from tests.market.fixtures.usecases.scenarios.ver1 import Bridge

__all__ = [
    "business_has_address",
]

business_has_address = Bridge(
    _previous=None,
    _current=business_has_address_ft
)
