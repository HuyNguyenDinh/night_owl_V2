from tests.market.fixtures.usecases.scenarios.ver1 import Fixture
from market.models import CartDetail

__all__ = [
    "cart_detail_ft"
]

cart_detail_ft = Fixture(
    _instance=CartDetail.recipe()
)
