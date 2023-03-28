from tests.market.fixtures.usecases.scenarios.ver1 import Fixture
from market.models import Picture

__all__ = [
    "option_picture_ft"
]

option_picture_ft = Fixture(
    _instance=Picture.recipe()
)
