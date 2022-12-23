from tests.market.fixtures.models.base_recipes import *
from tests.market.fixtures.recipe_setups import *
from tests.market.fixtures.entities.options import *

empty_option_picture_video = set_recipe_relationship(
    general_product_option_picture,
    product_option=product_option_empty
)

full_option_picture_video = set_recipe_relationship(
    general_product_option_picture,
    product_option=product_option_full
)