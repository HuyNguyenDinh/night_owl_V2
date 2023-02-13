from model_bakery import seq
from tests.market.fixtures.usecases.scenarios.ver1 import Fixture
from tests.market.fixtures.entities.vouchers import percentage_voucher, not_percentage_voucher
import random
import string

__all__ = [
    "percentage_vouchers_ft",
    "percentage_voucher_ft",
    "not_percentage_voucher_ft",
]


def random_code(n: int = 24) -> str:
    return ''.join(random.choices(string.ascii_letters, k=n))


percentage_voucher_ft = Fixture(
    _instance=percentage_voucher,
    _recipe_params={
        'code': random_code
    }
)

percentage_vouchers_ft = percentage_voucher_ft.fixture_extend(
    _recipe_params={
        'code': seq('voucher'),
        '_quantity': 3
    }
)

not_percentage_voucher_ft = percentage_voucher_ft.fixture_extend(
    _instance=not_percentage_voucher
)

not_percentage_vouchers_ft = not_percentage_voucher_ft.fixture_extend(
    _recipe_params={
        'code': seq('voucher'),
        '_quantity': 3
    }
)
