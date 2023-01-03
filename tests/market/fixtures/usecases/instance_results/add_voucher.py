from tests.market.fixtures.entities.vouchers import *
from tests.market.fixtures.usecases.scenarios.ver1 import *
from model_bakery.recipe import seq
import random, string

def random_code(n: int = 24) -> str:
    return ''.join(random.choices(string.ascii_letters, k=n))

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

not_percentage_voucher_bridge= Bridge(
    _previous=None,
    _current=not_percentage_voucher_fixture
)

