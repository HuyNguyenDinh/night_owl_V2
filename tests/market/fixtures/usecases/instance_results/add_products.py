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

class AddProductFT(AddVoucherFT, SellingFT):

    def prepare_fixtures(self):
        print('fixture - 3')
        super().prepare_fixtures()
        self.fixtures['product_fixture'] = Fixture(
            _instance=general_product
        )

        self.fixtures['products_fixture'] = self.fixtures.get('product_fixture').fixture_extend(
            _recipe_params={
                '_quantity': 3
            }
        )

    def prepare_bridges(self):
        print('bridge - 3')
        super().prepare_bridges()
        self.bridges['product_valid'] = Bridge(
            _previous={
                'owner': self.bridges.get('business_has_address')
            },
            _current=self.fixtures.get('product_fixture')
        )

        self.bridges['product_percentage_valid'] = self.bridges.get('product_valid').bridge_extend(
            _previous={
                'owner': self.bridges.get('business_has_address'),
                'voucher_set': self.bridges.get('percentage_vouchers_bridge')
            }
        )

        self.bridges['products_valid'] = self.bridges.get('product_valid').bridge_extend(
            _current=products_fixture
        )

        self.bridges['products_percentage_voucher_valid'] = self.bridges.get('products_valid').bridge_extend(
            _previous={
                'owner': self.bridges.get('business_has_address'),
                'voucher_set': self.bridges.get('percentage_vouchers_bridge')
            }
        )

        self.bridges['products_not_percentage_voucher_valid'] = self.bridges.get('products_valid').bridge_extend(
            _previous={
                'owner': self.bridges.get('business_has_address'),
                'voucher_set': self.bridges.get('not_percentage_vouchers_bridge')
            }
        )

    def get_bridge(self):
        self.bridges.get('product_valid').get_fixture()
        self.bridges.get('product_percentage_valid').get_fixture()
        self.bridges.get('products_valid').get_fixture()
        self.bridges.get('products_percentage_voucher_valid').get_fixture()
        self.bridges.get('products_not_percentage_voucher_valid').get_fixture()
