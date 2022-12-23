from model_bakery.recipe import Recipe, seq, foreign_key
from market.models import *

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
    "general_product_option_picture"
]

general_user = Recipe(User)
general_address = Recipe(Address, note='abc')
general_product = Recipe(Product, description='abc')
general_product_option = Recipe(Option, unit_in_stock=100)
general_cart_detail = Recipe(CartDetail)
general_order = Recipe(Order, note='abc')
general_order_detail = Recipe(OrderDetail, quantity=1, unit_price=1)
general_bill = Recipe(Bill)
general_rating= Recipe(Rating, comment='abc')
general_report = Recipe(Report, content='abc')
general_reply = Recipe(Reply, content='abc')
general_category = Recipe(Category)
general_voucher = Recipe(Voucher)
general_product_option_picture = Recipe(Picture)

__recipe__ = [
    general_user,
    general_address,
    general_product,
    general_product_option,
    general_order,
    general_order_detail,
    general_bill,
    general_cart_detail,
    general_rating,
    general_report,
    general_reply,
    general_category,
    general_voucher,
    general_product_option_picture
]