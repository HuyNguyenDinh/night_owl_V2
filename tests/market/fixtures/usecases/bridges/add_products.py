from tests.market.fixtures.usecases.scenarios.ver1 import Bridge
from tests.market.fixtures.usecases.fixtures import add_products
from tests.market.fixtures.usecases.bridges import selling
from tests.market.fixtures.usecases.bridges import add_voucher
import itertools
from tests.market.fixtures.usecases.scenarios.ver2 import use_case

__all__ = [
    "product_valid",
    "products_valid",
    # "product_percentage_voucher_valid",
    # "product_not_percentage_voucher_valid",
    # "products_percentage_vouchers_valid",
    # "products_not_percentage_vouchers_valid",
    # "products_percentage_voucher_valid",
    # "products_not_percentage_voucher_valid"
]

product_valid = Bridge(
    _previous={
        'owner': selling.business_has_address
    },
    _current=add_products.product_ft
)

products_valid = product_valid.bridge_extend(
    _current=add_products.products_ft
)

# product_percentage_voucher_valid = product_valid.bridge_extend(
#     _previous={
#         'owner': selling.business_has_address,
#         'voucher_set': add_voucher.percentage_voucher
#     }
# )
#
# products_percentage_voucher_valid = products_valid.bridge_extend(
#     _previous={
#         'owner': selling.business_has_address,
#         'voucher_set': add_voucher.percentage_voucher
#     }
# )
#
# products_percentage_vouchers_valid = products_valid.bridge_extend(
#     _previous={
#         'owner': selling.business_has_address,
#         'voucher_set': add_voucher.percentage_vouchers
#     }
# )
#
# product_not_percentage_voucher_valid = product_valid.bridge_extend(
#     _previous={
#         'owner': selling.business_has_address,
#         'voucher_set': add_voucher.not_percentage_voucher
#     }
# )
#
# products_not_percentage_voucher_valid = products_valid.bridge_extend(
#     _previous={
#         'owner': selling.business_has_address,
#         'voucher_set': add_voucher.not_percentage_voucher
#     }
# )
#
# products_not_percentage_vouchers_valid = products_not_percentage_voucher_valid.bridge_extend(
#     _previous={
#         'owner': selling.business_has_address,
#         'voucher_set': add_voucher.not_percentage_vouchers
#     }
# )

# __bridge__ = (i[0].bridge_extend(
#     _previous={
#         'owner': selling.business_has_address,
#         'voucher_set': i[1]
#     }) for i in itertools.product([product_valid, products_valid], add_voucher.__bridge__))

__bridge__ = use_case(
    fixtures=[add_products.product_ft, add_products.products_ft],
    previous_bridges={
     'voucher_set': add_voucher.__bridge__,
     'owner': [selling.business_has_address],
    }
)
