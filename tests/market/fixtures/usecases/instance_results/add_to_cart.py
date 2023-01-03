from tests.market.fixtures.entities.cartdetail import *
from tests.market.fixtures.usecases.instance_results.add_options import *
from tests.market.fixtures.usecases.instance_results.buying import *
from market.baker_recipes import *
from market.models import *

cart_detail_fixture = Fixture(
    _instance=general_cart_detail
)

cart_detail_fixtures = cart_detail_fixture.fixture_extend(
    _recipe_params={
        '_quantity': 3
    }
)

valid_cart_detail = Bridge(
    _previous={
        'product_option': valid_product_option_full,
        'customer': customer_has_address
    },
    _current=cart_detail_fixture
)

valid_cart_details = valid_cart_detail.bridge_extend(
    _current=cart_detail_fixtures
)

# def valid_cart_detail(**kwargs) -> CartDetail | List[CartDetail]:
#     return cart_detail_instance(general_cart_detail, valid_product_option_full(), customer_has_address(), **kwargs)
#
# def multi_valid_cart_detail_of_product(_quantity: int = 3, **kwargs) -> List[CartDetail]:
#     return cart_detail_instances(
#         general_cart_detail,
#         multi_valid_product_option_full(_quantity=_quantity),
#         customer_has_address(),
#         **kwargs
#     )
#
# def multi_valid_carts_of_customer(_quantity_store: int = 3, _quantity_option_each_one: int = 3, **kwargs) -> List[CartDetail]:
#     list_carts: List[CartDetail] = []
#     _customer = customer_has_address()
#     for _ in range(_quantity_store):
#         temp_cart = cart_detail_instances(
#             general_cart_detail,
#             multi_valid_product_option_full(_quantity=_quantity_option_each_one),
#             _customer
#         )
#         [list_carts.append(i) for i in temp_cart]
#     return list_carts
