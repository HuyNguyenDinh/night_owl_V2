from tests.market.fixtures.usecases.instance_results.buying import user_has_address_instance
from tests.market.fixtures.entities.users import *
from tests.market.fixtures.entities.addresses import *
from model_bakery.recipe import Recipe
from market.models import *
from typing import List
from tests.market.fixtures.usecases.scenarios.ver1 import *
from tests.market.fixtures.usecases.scenarios.ver2 import Chain, Node


class SellingNode(Node):
    def __init__(self):
        super().__init__()
        self.fixtures.business_fixture = Fixture(
            _instance=business,
            _reverse_relationship_recipe={
                'address': ('creator', q7_address)
            }
        )
        self.bridges.business_has_address = Bridge(
            _previous=None,
            _current=business_fixture
        )


selling_fixtures: Dict[str, Fixture] = {
    'business_fixture': Fixture(
        _instance=business,
        _reverse_relationship_recipe={
            'address': ('creator', q7_address),
        }
    ),
}
business_fixture = Fixture(
    _instance=business,
    _reverse_relationship_recipe={
        'address': ('creator', q7_address)
    }
)

selling_bridges: Dict[str, Bridge] = {
    'business_has_address': Bridge(
        _previous=None,
        _current=selling_fixtures.get('business_fixture')
    )
}

business_has_address = Bridge(
    _previous=None,
    _current=business_fixture
)


class SellingFT(OnePiece):
    def prepare_fixtures(self):
        super().prepare_fixtures()
        self.fixtures['business_fixture'] = Fixture(
            _instance=business,
            _reverse_relationship_recipe={
                'address': ('creator', q7_address)
            }
        )

    def prepare_bridges(self):
        super().prepare_bridges()
        self.bridges['business_has_address'] = Bridge(
            _previous=None,
            _current=self.fixtures.get('business_fixture')
        )

    def get_bridge(self):
        self.bridges['business_has_address'].get_fixture()


class SellingChain(Chain):
    def prepare_fixtures(self):
        self.fixtures['business_fixture'] = Fixture(
            _instance=business,
            _reverse_relationship_recipe={
                'address': ('creator', q7_address)
            }
        )

    def prepare_bridges(self):
        self.bridges['business_has_address'] = Bridge(
            _previous=None,
            _current=self.get_fixture_by_name('business_fixture')
        )
