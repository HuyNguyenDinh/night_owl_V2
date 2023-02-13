from tests.market.fixtures.usecases.scenarios.ver1 import Fixture
from market.models import Product

__all__ = [
    "product_ft",
    "products_ft"
]

product_ft = Fixture(
    _instance=Product.recipe()
)

products_ft = product_ft.fixture_extend(
    _recipe_params={
        '_quantity': 3
    }
)
