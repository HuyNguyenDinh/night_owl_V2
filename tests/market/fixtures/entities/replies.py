from market.models import *
from model_bakery.recipe import Recipe
from typing import List

def reply_instance(_reply_recipe: Recipe, _report: Report, _creator: User, **kwargs) -> Reply | List[Reply]:
    return _reply_recipe.make(report=_report, creator=_creator, **kwargs)