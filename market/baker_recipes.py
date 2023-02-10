from model_bakery.recipe import Recipe, foreign_key, related, seq
from .models import *
from django.contrib.auth import get_user_model
import decimal

user_model = get_user_model()

user_huy = Recipe(
    user_model,
    email=seq("huyn2731", suffix="@gmail.com"),
    phone_number=seq("093746132"),
    email_verified=True,
    phone_verified=True,
    is_business=True,
)

user_normal = Recipe(
    user_model,
    email=seq("nightowl.usernormal.", suffix="@gmail.com"),
    phone_number=seq("8493746132"),
    email_verified=True,
    phone_verified=True,
)

huy_address = Recipe(
    Address,
    province_id=202,
    district_id=1449,
    ward_id="20709",
    street="Bùi Văn Ba",
    full_address="Bùi Văn Ba, Phường Tân Thuận Đông, Quận 7, Hồ Chí Minh",
)

user_normal_address = Recipe(
    Address,
    province_id=204,
    district_id=1536,
    ward_id="480126",
    street="67/13 Hoàng Minh Chánh",
    full_address="67/13 Hoàng Minh Chánh, phường Hóa An, TP Biên Hòa, Đồng Nai",
    note="abc",
)

#################################################################################

__all__ = [
    "general_user",
    "general_address",
    "general_product",
    "general_product_option",
    "general_order",
    "general_order_detail",
    "general_bill",
    "general_cart_detail",
    "general_rating",
    "general_report",
    "general_reply",
    "general_category",
    "general_voucher",
    "general_product_option_picture",
    "user_huy",
    "user_normal",
    "huy_address",
    "user_normal_address",
]

general_user = Recipe(User)
general_address = Recipe(Address, note="abc")
general_product = Recipe(Product, description="abc")
general_product_option = Recipe(Option, unit_in_stock=100)
general_cart_detail = Recipe(CartDetail)
general_order = Recipe(Order, note="abc")
general_order_detail = Recipe(OrderDetail, quantity=1, unit_price=1)
general_bill = Recipe(Bill)
general_rating = Recipe(Rating, comment="abc")
general_report = Recipe(Report, content="abc")
general_reply = Recipe(Reply, content="abc")
general_category = Recipe(Category)
general_voucher = Recipe(Voucher)
general_product_option_picture = Recipe(Picture)
