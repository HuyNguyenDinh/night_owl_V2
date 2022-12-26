from market.baker_recipes import *
from tests.market.fixtures.recipe_setups import *
from tests.market.fixtures.entities.options import *
from tests.market.fixtures.usecases.recipes.add_options import *

empty_option_picture_video = general_product_option_picture.make(product_option=valid_product_option_emtpy)

full_option_picture_video = general_product_option_picture.make(product_option=valid_product_option_full)