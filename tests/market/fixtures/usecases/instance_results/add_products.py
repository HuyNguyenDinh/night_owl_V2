from tests.market.fixtures.usecases.instance_results.selling import business_has_address
from tests.market.fixtures.entities.products import *
from tests.market.fixtures.usecases.scenarios.ver1 import *
from tests.market.fixtures.usecases.instance_results.add_voucher import *
from tests.market.fixtures.usecases.instance_results.selling import *

product_fixture = Fixture(
    _instance=general_product
)

products_fixture = product_fixture.fixture_extend(
    _recipe_params={
        '_quantity': 3
    }
)

product_valid = Bridge(
    _previous={
        'owner': business_has_address
    },
    _current=product_fixture
)

product_percentage_valid = product_valid.bridge_extend(
    _previous={
        'owner': business_has_address,
        'voucher_set': percentage_vouchers_bridge
    }
)

products_valid = product_valid.bridge_extend(
    _current=products_fixture
)

products_percentage_voucher_valid = products_valid.bridge_extend(
    _previous={
        'owner': business_has_address,
        'vouchers': percentage_voucher_bridge
    }
)

products_not_percentage_voucher_valid = products_valid.bridge_extend(
    _previous={
        'owner': business_has_address,
        'vouchers': not_percentage_voucher_bridge
    }
)
