from abc import ABC
from model_bakery.recipe import Recipe, foreign_key

def set_recipe_relationship(_recipe: Recipe, **kwargs: Recipe):
    relationships = dict()
    for key, value in kwargs.items():
        relationships[key] = foreign_key(value)
    return _recipe.extend(**relationships)
