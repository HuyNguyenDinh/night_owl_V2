from market.baker_recipes import *
from tests.market.fixtures.entities.users import *
from tests.market.fixtures.entities.valid_logic import *

business_has_address = q7_address.make(creator=business.make()).creator
