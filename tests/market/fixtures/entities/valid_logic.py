from tests.market.fixtures.entities.users import *
from tests.market.fixtures.models.base_recipes import *
from model_bakery.recipe import foreign_key

__all__ = [
    "valid_cart_detail",
    "valid_order",
    "valid_order_detail",
    "valid_bill",
    "q7_address",
    "bh_address"
]

valid_cart_detail = general_cart_detail.extend(customer=foreign_key(customer), product_option=foreign_key(business_product_option))
valid_order = general_order.extend(store=foreign_key(business), customer=foreign_key(customer))
valid_order_detail = general_order_detail.extend(order=foreign_key(valid_order), product_option=foreign_key(business_product_option))
valid_bill = general_bill.extend(value=1, order_payed=foreign_key(valid_order), customer=foreign_key(customer))
valid_report = general_report.extend(reporter=foreign_key(general_user))
valid_reply = general_reply.extend(report=foreign_key(valid_report), creator=foreign_key(general_user))

q7_address = general_address.extend(province_id=202, district_id=1449, ward_id="20709", street="Bùi Văn Ba",
                                    full_address="Bùi Văn Ba, Phường Tân Thuận Đông, Quận 7, Hồ Chí Minh")
bh_address = general_address.extend(province_id=204, district_id=1536, ward_id="480126", street="67/13 Hoàng Minh Chánh",
                                    full_address="67/13 Hoàng Minh Chánh, phường Hóa An, TP Biên Hòa, Đồng Nai", note='abc')

__recipe__ = [
    valid_cart_detail,
    valid_order,
    valid_order_detail,
    valid_bill,
    q7_address,
    bh_address
]