from tests.market.fixtures.models.base_recipes import general_product_option
from django.db.models.fields import BigIntegerField

product_option_empty = general_product_option.extend(unit_in_stock=0)
product_option_full = general_product_option.extend(unit_in_stock=BigIntegerField.MAX_BIGINT)