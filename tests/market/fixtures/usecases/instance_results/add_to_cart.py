from tests.market.fixtures.entities.cartdetail import *
from tests.market.fixtures.usecases.instance_results.add_options import *
from tests.market.fixtures.usecases.instance_results.buying import *
from market.baker_recipes import *
from market.models import *

cart_detail_fixture = Fixture(
    _instance=CartDetail.recipe()
)

def new_option():
    return valid_product_option_full.bridge_extend().get_fixture()

cart_detail_fixtures = Fixture(
    _instance=general_cart_detail,
    _recipe_params={
        '_quantity': 5,
        'product_option': new_option
    }
)

valid_cart_detail = Bridge(
    _previous={
        'product_option': valid_product_option_full,
        'customer': customer_has_address
    },
    _current=cart_detail_fixture
)

valid_cart_details = Bridge(
    _previous={
        'customer': customer_has_address
    },
    _current=cart_detail_fixtures
)

class AddToCartFT(AddOptionFT, BuyingFT):
    def prepare_fixtures(self):
        super().prepare_fixtures()
        self.fixtures['cart_detail_fixture'] = Fixture(
            _instance=CartDetail.recipe()
        )

        self.fixtures['cart_detail_fixtures'] = self.fixtures.get('cart_detail_fixture').fixture_extend(
            _recipe_params={
                '_quantity': 5,
                'product_option': self.new_option
            }
        )
    @classmethod
    def new_option(cls):
        return valid_product_option_full.bridge_extend().get_fixture()

    def prepare_bridges(self):
        super().prepare_bridges()
        self.bridges['valid_cart_detail'] = Bridge(
            _previous={
                'product_option': self.bridges.get('valid_product_option_full'),
                'customer': self.bridges.get('customer_has_address')
            },
            _current=self.fixtures.get('cart_detail_fixture')
        )

        self.bridges['valid_cart_details'] = Bridge(
            _previous={
                'customer': self.bridges.get('customer_has_address')
            },
            _current=self.fixtures.get('cart_detail_fixtures')
        )

    def get_bridge(self):
        self.bridges.get('valid_cart_detail').get_fixture()
        self.bridges.get('valid_cart_details').get_fixture()