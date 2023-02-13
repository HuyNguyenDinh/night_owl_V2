from tests.market.fixtures.usecases.scenarios.ver1 import Bridge
from tests.market.fixtures.usecases.fixtures import add_voucher

__all__ = [
    "percentage_voucher",
    "percentage_vouchers",
    "not_percentage_voucher",
]

percentage_voucher = Bridge(
    _previous=None,
    _current=add_voucher.percentage_voucher_ft
)

percentage_vouchers = Bridge(
    _previous=None,
    _current=add_voucher.percentage_vouchers_ft
)

not_percentage_voucher = Bridge(
    _previous=None,
    _current=add_voucher.not_percentage_voucher_ft
)

not_percentage_vouchers = Bridge(
    _previous=None,
    _current=add_voucher.not_percentage_vouchers_ft
)

__bridge__ = [
    percentage_voucher,
    percentage_vouchers,
    not_percentage_voucher,
    not_percentage_vouchers,
]
