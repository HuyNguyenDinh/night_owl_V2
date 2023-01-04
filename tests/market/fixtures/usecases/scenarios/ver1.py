from typing import TypeVar, List, Union, Dict, Tuple, Any
from model_bakery.recipe import Recipe
from django.db.models import Model

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
                relationship_field: Recipe of Model,
                ...
            },
            _relationship: {
                relationship_field: Instance of Model,
                ...
            }
            _reverse_relationship_recipe: {
                reverse relationship: Tuple('relationship field in reverse object', Recipe of Model),
                ...
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
        self._instance: Union[Recipe, M | List[M]] = _instance.extend()
        self.relationship_recipe = {}
        if _relationship_recipe:
            for key, rela_recipe in _relationship_recipe.items():
                self.relationship_recipe[key] = rela_recipe.extend()
        self.relationship = _relationship
        self.reverse_relationship_recipe = {}
        if _reverse_relationship_recipe:
            for key, rev_rela_recipe in _reverse_relationship_recipe.items():
                self.reverse_relationship_recipe[key] = (rev_rela_recipe[0], rev_rela_recipe[1].extend())
        self.recipe_params = _recipe_params
        self.isInstance = False

    def _prepare(self, **kwargs):
        """
            Make Instance with relationship
        """
        if self.relationship_recipe:
            for key, recipe in self.relationship_recipe.items():
                self.relationship_recipe[key] = recipe.make()
        if self.relationship:
            if self.recipe_params:
                if self.relationship_recipe:
                    self._instance = self._instance.make(
                        **self.relationship_recipe,
                        **self.relationship,
                        **self.recipe_params,
                        **kwargs
                    )
                else:
                    self._instance = self._instance.make(
                        **self.relationship,
                        **self.recipe_params,
                        **kwargs
                    )
            else:
                if self.relationship_recipe:
                    self._instance = self._instance.make(
                        **self.relationship_recipe,
                        **self.relationship,
                        **kwargs
                    )
                else:
                    self._instance = self._instance.make(
                        **self.relationship,
                        **kwargs
                    )
        else:
            if self.recipe_params:
                if self.relationship_recipe:
                    self._instance = self._instance.make(
                        **self.relationship_recipe,
                        **self.recipe_params,
                        **kwargs
                    )
                else:
                    self._instance = self._instance.make(
                        **self.recipe_params,
                        **kwargs
                    )
            else:
                self._instance = self._instance.make(**kwargs)
        self.isInstance = True

    def fixture_extend(self,
                       _instance: Union[Recipe, None] = None,
                       _relationship_recipe: Union[Dict[str, Recipe], None] = None,
                       _relationship: Union[Dict[str, M | List[M]], None] = None,
                       _reverse_relationship_recipe: Union[Dict[str, Tuple[str, Recipe]], None] = None,
                       _recipe_params: Union[Dict[str, Any], None] = None) -> 'Fixture':
        if self.isInstance:
            raise ValueError
        attribute = {
            '_instance': _instance,
            '_relationship_recipe': _relationship_recipe,
            '_relationship': _relationship,
            '_reverse_relationship_recipe': _reverse_relationship_recipe,
            '_recipe_params': _recipe_params
        }
        for key, value in attribute.items():
            if value:
                continue
            att = key[1:]
            if key != '_instance':
                if hasattr(self, att):
                    v = getattr(self, att)
                    attribute[key] = v
            else:
                if hasattr(self, '_instance'):
                    v = getattr(self, '_instance')
                    attribute[key] = v
        return Fixture(**attribute)

    def set_instance(self, _instance: M | List[M]):
        self._instance = _instance
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
    def __init__(self,
                 _previous: Union[Dict[str, 'Bridge'], None],
                 _current: Fixture):
        """
            _previous: {
                <relationship_field>: Bridge,
                ...
            }
            _current: The Fixture make from recipe which can include relationship
        """
        self._previous = {}
        if _previous:
            for key, bridge in _previous.items():
                self._previous[key] = bridge.bridge_extend()
        self._current = _current.fixture_extend()
        self._isMake = False

    def _make_relate(self, **kwargs):
        temp_relate = {}
        for pre_key, pre_bridge in self._previous.items():
            temp_relate[pre_key] = pre_bridge.get_fixture()
        self._current.make_instance(**temp_relate, **kwargs)

    def _make_fixtures(self, **kwargs):
        if self._previous:
            self._make_relate(**kwargs)
        self._isMake = True

    def bridge_extend(self,
                      _previous: Union[Dict[str, 'Bridge'], None] = None,
                      _current: Union[Fixture, None] = None) -> 'Bridge':
        if self._isMake:
            raise ValueError
        if _previous:
            for key, bridge in _previous.items():
                _previous[key] = bridge.bridge_extend()
            if _current:
                return Bridge(_previous, _current.fixture_extend())
            return Bridge(_previous, self._current.fixture_extend())
        if self._previous:
            temp_previous = {}
            for key, bridge in self._previous.items():
                temp_previous[key] = bridge.bridge_extend()
            if _current:
                return Bridge(temp_previous, _current.fixture_extend())
            return Bridge(temp_previous, self._current.fixture_extend())
        return Bridge(None, self._current.fixture_extend())

    def get_fixture(self, **kwargs) -> M | List[M]:
        if not self._isMake:
            self._make_fixtures(**kwargs)
        return self._current.make_instance()

class Piece:
    def __init__(self):
        self.fixtures: Dict[str, Fixture] = {}
        self.bridges: Dict[str, Bridge] = {}
    def prepare_fixtures(self):
        print('fixture - 1')
        pass
    def prepare_bridges(self):
        print('bridge - 1')
        pass
    def get_bridge(self):
        pass

class OnePiece(Piece):
    def prepare(self):
        self.prepare_fixtures()
        self.prepare_bridges()
        self.get_bridge()