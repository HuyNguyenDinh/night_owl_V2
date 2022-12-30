from model_bakery.recipe import Recipe
from market.models import User, Address
from market.baker_recipes import *


def address_instance(_address_recipe: Recipe, _user: User, **kwargs) -> Address:
    return _address_recipe.make(creator=_user, **kwargs)

q7_address = general_address.extend(province_id=202, district_id=1449, ward_id="20709", street="Bùi Văn Ba",
                                    full_address="Bùi Văn Ba, Phường Tân Thuận Đông, Quận 7, Hồ Chí Minh")
bh_address = general_address.extend(province_id=204, district_id=1536, ward_id="480126", street="67/13 Hoàng Minh Chánh",
                                    full_address="67/13 Hoàng Minh Chánh, phường Hóa An, TP Biên Hòa, Đồng Nai", note='abc')