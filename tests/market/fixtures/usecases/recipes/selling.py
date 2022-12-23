from tests.market.fixtures.models.base_recipes import *
from tests.market.fixtures.entities.users import *
from tests.market.fixtures.entities.valid_logic import *

business_has_address = business.extend(address=q7_address)