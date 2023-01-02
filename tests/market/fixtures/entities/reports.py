from market.models import *
from model_bakery.recipe import Recipe
from typing import List

def report_instance(_report_recipe: Recipe, _reporter: User, **kwargs) -> Report | List[Report]:
    return _report_recipe.make(reporter=_reporter, **kwargs)