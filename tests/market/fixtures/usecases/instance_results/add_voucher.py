from tests.market.fixtures.entities.vouchers import *
from tests.market.fixtures.usecases.scenarios.ver1 import *
from tests.market.fixtures.usecases.scenarios.ver2 import Chain, Node
from model_bakery.recipe import seq
import random
import string


def random_code(n: int = 24) -> str:
    return ''.join(random.choices(string.ascii_letters, k=n))


class AddVoucherNode(Node):
    def __init__(self):
        super().__init__()
        self.fixtures.percentage_voucher = Fixture(
            _instance=percentage_voucher,
            _recipe_params={
                'code': self.random_code()
            }
        )
        self.fixtures.percentage_vouchers = Fixture(
            _instance=not_percentage_voucher,
            _recipe_params={
                'code': self.random_code()
            }
        )
        self.fixtures.not_percentage_voucher = Fixture(
            _instance=not_percentage_voucher,
            _recipe_params={
                'code': random_code()
            }
        )
        self.bridges.percentage_voucher_bridge = Bridge(
            _previous=None,
            _current=self.fixtures.percentage_voucher
        )

        self.bridges.percentage_vouchers_bridge = Bridge(
            _previous=None,
            _current=self.fixtures.percentage_vouchers
        )

        self.bridges.not_percentage_voucher_bridge = Bridge(
            _previous=None,
            _current=self.fixtures.not_percentage_voucher
        )

        self.currents = [
            self.bridges.percentage_vouchers_bridge,
            self.bridges.percentage_voucher_bridge,
            self.bridges.not_percentage_voucher_bridge
        ]

    @classmethod
    def random_code(cls, n: int = 24) -> str:
        return ''.join(random.choices(string.ascii_letters, k=n))


add_voucher_fixtures: Dict[str, Fixture] = {
    'percentage_voucher': Fixture(
        _instance=percentage_voucher,
        _recipe_params={
            'code': random_code()
        }
    ),
    'percentage_vouchers': Fixture(
        _instance=percentage_voucher,
        _recipe_params={
            'code': seq('voucher'),
            '_quantity': 3,
        }
    ),
    'not_percentage_voucher_fixture': Fixture(
        _instance=not_percentage_voucher,
        _recipe_params={
            'code': random_code()
        }
    )
}
percentage_voucher_fixture = Fixture(
    _instance=percentage_voucher,
    _recipe_params={
        'code': random_code()
    }
)

percentage_vouchers_fixture = percentage_voucher_fixture.fixture_extend(
    _recipe_params={
        'code': seq('voucher'),
        '_quantity': 3
    }
)

not_percentage_voucher_fixture = percentage_voucher_fixture.fixture_extend(
    _instance=not_percentage_voucher
)

percentage_voucher_bridge = Bridge(
    _previous=None,
    _current=percentage_voucher_fixture
)

percentage_vouchers_bridge = Bridge(
    _previous=None,
    _current=percentage_vouchers_fixture
)

not_percentage_voucher_bridge = Bridge(
    _previous=None,
    _current=not_percentage_voucher_fixture
)

class AddVoucherFT(OnePiece):
    @classmethod
    def random_code(cls, n: int = 24) -> str:
        return ''.join(random.choices(string.ascii_letters, k=n))
    def prepare_fixtures(self):
        super().prepare_fixtures()
        self.fixtures['percentage_voucher_fixture'] = Fixture(
            _instance=percentage_voucher,
            _recipe_params={
                'code': self.random_code,
            }
        )
        self.fixtures['percentage_vouchers_fixture'] = self.fixtures.get('percentage_voucher_fixture').fixture_extend(
            _recipe_params={
                'code': self.random_code,
                '_quantity': 3
            }
        )
        self.fixtures['not_percentage_voucher_fixture'] = self.fixtures.get('percentage_voucher_fixture').fixture_extend(
            _instance=not_percentage_voucher
        )

        self.fixtures['not_percentage_voucher_fixtures'] = self.fixtures.get('not_percentage_voucher_fixture').fixture_extend(
            _recipe_params={
                'code': self.random_code,
                '_quantity': 3
            }
        )

    def prepare_bridges(self):
        super().prepare_bridges()
        self.bridges['percentage_voucher_bridge'] = Bridge(
            _previous=None,
            _current=self.fixtures.get('percentage_voucher_fixture')
        )

        self.bridges['percentage_vouchers_bridge'] = Bridge(
            _previous=None,
            _current=self.fixtures.get('percentage_vouchers_fixture')
        )

        self.bridges['not_percentage_voucher_bridge']= Bridge(
            _previous=None,
            _current=self.fixtures.get('not_percentage_voucher_fixture')
        )
        self.bridges['not_percentage_vouchers_bridge'] = Bridge(
            _previous=None,
            _current=self.fixtures.get('not_percentage_voucher_fixtures')
        )

    def get_bridge(self):
        self.bridges.get('percentage_voucher_bridge').get_fixture()
        self.bridges.get('percentage_vouchers_bridge').get_fixture()
        self.bridges.get('not_percentage_voucher_bridge').get_fixture()
        self.bridges.get('not_percentage_vouchers_bridge').get_fixture()

class AddVoucherChain(Chain):
    @classmethod
    def random_code(cls, n: int = 24) -> str:
        return ''.join(random.choices(string.ascii_letters, k=n))
    def prepare_fixtures(self):
        self.fixtures['percentage_voucher_fixture'] = Fixture(
            _instance=percentage_voucher,
            _recipe_params={
                'code': self.random_code,
            }
        )
        self.fixtures['percentage_vouchers_fixture'] = self.get_fixture_by_name('percentage_voucher_fixture').fixture_extend(
            _recipe_params={
                'code': self.random_code,
                '_quantity': 3
            }
        )
        self.fixtures['not_percentage_voucher_fixture'] = self.get_fixture_by_name('percentage_voucher_fixture').fixture_extend(
            _instance=not_percentage_voucher
        )

        self.fixtures['not_percentage_voucher_fixtures'] = self.get_fixture_by_name('not_percentage_voucher_fixture').fixture_extend(
            _recipe_params={
                'code': self.random_code,
                '_quantity': 3
            }
        )

    def prepare_bridges(self):
        self.bridges['percentage_voucher_bridge'] = Bridge(
            _previous=None,
            _current=self.get_fixture_by_name('percentage_voucher_fixture')
        )

        self.bridges['percentage_vouchers_bridge'] = Bridge(
            _previous=None,
            _current=self.get_fixture_by_name('percentage_vouchers_fixture')
        )

        self.bridges['not_percentage_voucher_bridge']= Bridge(
            _previous=None,
            _current=self.get_fixture_by_name('not_percentage_voucher_fixture')
        )
        self.bridges['not_percentage_vouchers_bridge'] = Bridge(
            _previous=None,
            _current=self.get_fixture_by_name('not_percentage_voucher_fixtures')
        )