from model_bakery.recipe import Recipe, foreign_key, related, seq
from .models import *
from django.contrib.auth import get_user_model
import decimal

user_model = get_user_model()

user_huy = Recipe(user_model, email=seq("huyn2731" , suffix="@gmail.com"), phone_number=seq("093746132"), email_verified=True,
                  phone_verified=True, is_business=True)

user_normal = Recipe(user_model, email=seq("nightowl.usernormal.", suffix="@gmail.com"), phone_number=seq("8493746132"),
                     email_verified=True, phone_verified=True)

huy_address = Recipe(Address, province_id=202, district_id=1449, ward_id="20709", street="Bùi Văn Ba",
                     full_address="Bùi Văn Ba, Phường Tân Thuận Đông, Quận 7, Hồ Chí Minh")

user_normal_address = Recipe(Address, province_id=204, district_id=1536, ward_id="480126", street="67/13 Hoàng Minh Chánh",
                             full_address="67/13 Hoàng Minh Chánh, phường Hóa An, TP Biên Hòa, Đồng Nai", note='abc')

product = Recipe(Product, name='IPhone 14 Pro Max 512GB', sold_amount=10, description='abc')

product_option = Recipe(Option, unit_in_stock=50)

order = Recipe(Order, total_shipping_fee=25000, shipping_code='LLXHKE', note='abc')

order_detail = Recipe(OrderDetail, quantity=2)

bill = Recipe(Bill, value=200025000)

voucher = Recipe(Voucher, discount=decimal.Decimal(10), is_percentage=True)

cart = Recipe(CartDetail, quantity=2)

rating = Recipe(Rating, rate=4, comment='Test')