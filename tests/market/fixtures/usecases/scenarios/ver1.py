from abc import ABC, abstractmethod
from typing import TypeVar, List, Union, Dict, Tuple, Any
from model_bakery.recipe import Recipe
from django.db.models import Model
from tests.market.fixtures.entities.users import user_has_address_instance
from tests.market.fixtures.entities.products import product_instance
from tests.market.fixtures.entities.options import product_option_instance
from tests.market.fixtures.entities.option_pictures import option_with_picture_instance


M = TypeVar("M", bound=Model)


class Fixture:
    def __init__(self,
                 _instance: Recipe,
                 _relationship_recipe: Union[Dict[str, Recipe], None] = None,
                 _relationship: Union[Dict[str, M | List[M]], None] = None,
                 _reverse_relationship_recipe: Union[Dict[str, Tuple[str, Recipe]], None] = None,
                 _recipe_params: Union[Dict[str, Any], None] = None):
        """
            _relationship_recipe: {
                key[relationship_field]: value[Recipe of Model],
                ...
            },
            _relationship: {
                key[relationship_field]: value[Instance of Model],
                ...
            }
            _reverse_relationship_recipe: {
                key[reverse relationship]: value[{
                    key[relationship field in reverse object]: value[Recipe of Model],
                    ...
                }]
            },
            _recipe_params: {
                _quantity: int | None = None,
                make_m2m: bool | None = None,
                _refresh_after_create: bool | None = None,
                _create_files: bool | None = None,
                _using: str = "",
                _bulk_create: bool | None = None,
                _save_kwargs: dict[str, Any] | None = None,
                **attrs: Any
            }
        """
        self._instance: Union[Recipe, M | List[M]] = _instance
        self.relationship_recipe= _relationship_recipe
        self.relationship = _relationship
        self.reverse_relationship_recipe = _reverse_relationship_recipe
        self.recipe_params = _recipe_params
        self.isInstance = False

    def _prepare(self, **kwargs):
        """
            Make Instance with relationship
        """
        if self.relationship:
            if self.relationship_recipe:
                for key, recipe in self.relationship_recipe.items():
                    self.relationship_recipe[key] = recipe.make()
                self._instance = self._instance.make(
                    **self.relationship_recipe,
                    **self.relationship,
                    **self.recipe_params,
                    **kwargs
                )
            else:
                self._instance = self._instance.make(**self.relationship, **self.recipe_params, **kwargs)
        else:
            self._instance = self._instance.make(**self.recipe_params, **kwargs)
        self.isInstance = True

    def make_instance(self, **kwargs) -> M | List[M]:
        """
            Call _prepare() first to make instance
            -> Make reverse objects from instance
        """
        if not self.isInstance:
            self._prepare(**kwargs)
            if self.reverse_relationship_recipe:
                for key, recipe_field in self.reverse_relationship_recipe.items():
                    self.reverse_relationship_recipe[key] = recipe_field[1].make(**{recipe_field[0]: self._instance})
        return self._instance


class Bridge:
    def __init__(self, _previous: Union[Dict[str, 'Bridge'], None], _current: Fixture):
        self._previous = _previous
        self._current = _current
        self._isMake = False

    def make_relate(self):
        if self._previous:
            self._current.make_instance(**self._previous)

    def make_fixtures(self):
        if self._previous:
            for key, fixture in self._previous.items():
                self._previous[key] = fixture.get_fixture()
        self.make_relate()
        self._isMake = True

    def get_fixture(self) -> Fixture:
        if not self._isMake:
            self.make_fixtures()
        return self._current


# class UserWithAddress(Fixture):
#     pass
#
#
# class AddProduct(Bridge):
#     def make_relate(self):
#         self._current.make_instance()


# class AddOption(Fixture):
#     def __init__(self, _add_product: AddProduct, _option_recipe: Recipe, _quantity: int = 2):
#         self.add_product = _add_product
#         self.quantity = _quantity
#         super(Fixture, self).__init__(_option_recipe)
#     def get_instance(self) -> List[M]:
#         return product_option_instance(
#             _product_option_recipe=self.instance,
#             _product=self.add_product.get_instance(),
#             _quantity=self.quantity
#         )
#
# class AddOptionVideoPicture(Fixture):
#     def __init__(self, _add_option: AddOption, _option_image_recipe: Recipe):
#         self.add_option = _add_option
#         super(Fixture, self).__init__(_option_image_recipe)
#     def get_instance(self) -> List[M]:
#         temp_picture: List[M] = []
#         for option in self.add_option.get_instance():
#             temp_picture.append(option_with_picture_instance(
#                 self.instance,
#                 option
#             ))
#         return temp_picture