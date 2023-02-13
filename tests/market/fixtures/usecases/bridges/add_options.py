from tests.market.fixtures.usecases.scenarios.ver1 import Bridge
from tests.market.fixtures.usecases.fixtures import add_options
from tests.market.fixtures.usecases.bridges import add_products
import itertools

__bridge__ = (Bridge(
    _previous={
        'base_product': i[0]
    },
    _current=i[1]
) for i in itertools.product(add_products.__bridge__, add_options.__fixtures__))
