from tests.market.fixtures.entities.users import customer, user_has_address_instance
from tests.market.fixtures.entities.addresses import bh_address
from model_bakery.recipe import Recipe
from market.models import *
from typing import List
from tests.market.fixtures.usecases.scenarios.ver1 import *
from tests.market.fixtures.usecases.scenarios.ver2 import Chain

customer_fixture = Fixture(
    _instance=customer,
    _reverse_relationship_recipe={
        'address': ('creator', bh_address)
    }
)

customer_has_address = Bridge(
    _previous=None,
    _current=customer_fixture
)

class BuyingFT(OnePiece):
    def prepare_fixtures(self):
        super().prepare_fixtures()
        self.fixtures['customer_fixture'] = Fixture(
            _instance=customer,
            _reverse_relationship_recipe={
                'address': ('creator', bh_address)
            }
        )

    def prepare_bridges(self):
        super().prepare_bridges()
        self.bridges['customer_has_address'] = Bridge(
            _previous=None,
            _current=self.fixtures.get('customer_fixture')
        )

    def get_bridge(self):
        self.bridges.get('customer_has_address').get_fixture()

class BuyingChain(Chain):
    def prepare_fixtures(self):
        self.fixtures['customer_fixture'] = Fixture(
            _instance=customer,
            _reverse_relationship_recipe={
                'address': ('creator', bh_address)
            }
        )
    def prepare_bridges(self):
        self.bridges['customer_has_address'] = Bridge(
            _previous=None,
            _current=self.get_fixture_by_name('customer_fixture')
        )