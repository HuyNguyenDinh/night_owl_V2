from market.baker_recipes import *
from tests.market.fixtures.recipe_setups import *
from tests.market.fixtures.entities.options import *
from tests.market.fixtures.usecases.recipes.add_options import *
from tests.market.fixtures.entities.option_pictures import *

def empty_option_picture_video(**kwargs):
    return option_with_picture_instance(general_product_option_picture, valid_product_option_emtpy(), **kwargs)

def full_option_picture_video(**kwargs):
    return option_with_picture_instance(general_product_option_picture, valid_product_option_full(), **kwargs)