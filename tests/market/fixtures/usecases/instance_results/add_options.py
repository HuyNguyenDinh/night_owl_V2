from tests.market.fixtures.usecases.instance_results.add_products import *
from tests.market.fixtures.usecases.instance_results.add_voucher import *
from tests.market.fixtures.entities.options import *
from model_bakery.recipe import Recipe
from market.models import *
from typing import List
from tests.market.fixtures.usecases.scenarios.ver1 import *
from tests.market.fixtures.usecases.scenarios.ver2 import Chain

option_empty_fixture = Fixture(_instance=product_option_empty)
option_full_fixture = Fixture(_instance=product_option_full)
option_full_picture_fixture = Fixture(
    _instance=product_option_full,
    _reverse_relationship_recipe={
        'picture': ('product_option', general_product_option_picture)
    }
)

### Return product
valid_product_option_full = Bridge(
    _previous={
        'base_product': product_valid
    },
    _current=option_full_fixture
)

### Return [product1, product2, ...]
multi_valid_product_options_full = valid_product_option_full.bridge_extend(
    _current=option_empty_fixture.fixture_extend(
        _recipe_params={
            '_quantity': 3
        }
    )
)

multi_valid_product_voucher_options_full = multi_valid_product_options_full.bridge_extend(
    _previous={
        'base_product': product_percentage_valid
    }
)

class AddOptionFT(AddProductFT):
    def prepare_fixtures(self):
        super().prepare_fixtures()
        self.fixtures['option_empty_fixture'] = Fixture(_instance=product_option_empty)
        self.fixtures['option_full_fixture'] = Fixture(_instance=product_option_full)
        self.fixtures['option_full_picture_fixture'] = Fixture(
            _instance=product_option_full,
            _reverse_relationship_recipe={
                'picture': ('product_option', general_product_option_picture)
            }
        )

    def prepare_bridges(self):
        super().prepare_bridges()
        self.bridges['valid_product_option_full'] = Bridge(
            _previous={
                'base_product': self.bridges.get('product_valid')
            },
            _current=self.fixtures.get('option_full_fixture')
        )

        ### Return [product1, product2, ...]
        self.bridges['multi_valid_product_options_full'] = valid_product_option_full.bridge_extend(
            _current=self.fixtures.get('option_empty_fixture').fixture_extend(
                _recipe_params={
                    '_quantity': 3
                }
            )
        )

        self.bridges['multi_valid_product_voucher_options_full'] = multi_valid_product_options_full.bridge_extend(
            _previous={
                'base_product': self.bridges.get('product_percentage_valid')
            }
        )

    def get_bridge(self):
        self.bridges.get('valid_product_option_full').get_fixture()
        self.bridges.get('multi_valid_product_options_full').get_fixture()
        self.bridges.get('multi_valid_product_voucher_options_full').get_fixture()


class AddOptionChain(Chain):
    def prepare_fixtures(self):
        self.fixtures['option_empty_fixture'] = Fixture(_instance=product_option_empty)
        self.fixtures['option_full_fixture'] = Fixture(_instance=product_option_full)
        self.fixtures['option_full_picture_fixture'] = Fixture(
            _instance=product_option_full,
            _reverse_relationship_recipe={
                'picture': ('product_option', Picture.recipe())
            }
        )

    def prepare_bridges(self):
        self.bridges['valid_product_option_full'] = Bridge(
            _previous={
                'base_product': self.get_bridge_by_name('product_valid')
            },
            _current=self.get_fixture_by_name('option_full_fixture')
        )

        ### Return [product1, product2, ...]
        self.bridges['multi_valid_product_options_full'] = self.get_bridge_by_name('valid_product_option_full')\
            .bridge_extend(
                _current=self.get_fixture_by_name('option_empty_fixture').fixture_extend(
                    _recipe_params={
                        '_quantity': 3
                    }
                )
            )

        self.bridges['multi_valid_product_voucher_options_full'] = self.get_bridge_by_name('multi_valid_product_options_full')\
            .bridge_extend(
                _previous={
                    'base_product': self.get_bridge_by_name('product_percentage_valid')
                }
            )

    def prepare_previous(self):
        self.previous.append(AddProductChain())
