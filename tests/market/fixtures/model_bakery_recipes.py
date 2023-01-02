# from model_bakery import baker, recipe
# from abc import ABC
# from django.db.models import Model
# from unittest.case import TestCase
#
# __all__ = ["BaseModelBakeryFT", "BaseListModelBakerySameAttrFT", "BaseModelRecipeFT", "ListModelRecipeFT"]
#
# class BaseModelBakeryFT(ABC):
#     """
#         Object attribute save in self.obj with key is name attribute and value is the model instance in Database
#     """
#     @classmethod
#     def setUpClass(cls, _model: type[Model], attr: str, **kwargs) -> None:
#         if hasattr(cls, "obj"):
#             cls.obj.update({attr: baker.make(_model, **kwargs)})
#         else:
#             cls.obj = {attr: baker.make(_model, **kwargs)}
#
#
# class BaseListModelBakerySameAttrFT(ABC):
#     @classmethod
#     def setUpClass(cls, _model: type[Model], attr: str, **kwargs) -> None:
#         if hasattr(cls, "obj"):
#             cls.obj.update(attr, baker.make(_model, **kwargs))
#         else:
#             cls.obj = (attr, baker.make(_model, **kwargs))
#
#
# class BaseModelRecipeFT(ABC):
#     @classmethod
#     def setUpClass(cls, _recipe: recipe.Recipe, attr: str, **kwargs) -> None:
#         if hasattr(cls, "obj"):
#             cls.obj.update({attr: _recipe.make(**kwargs)})
#         else:
#             cls.obj = {attr: _recipe.make(**kwargs)}
#
#
# class ListModelRecipeFT(ABC):
#     @classmethod
#     def setUpClass(cls, attr_contain_list_instance: str, **kwargs: [str, recipe.Recipe]) -> None:
#         if hasattr(cls, "obj"):
#             if not cls.obj[attr_contain_list_instance]:
#                 cls.obj[attr_contain_list_instance] = {}
#             for key, value in kwargs.items():
#                 cls.obj[attr_contain_list_instance].update({key: value.make()})
#         else:
#             cls.obj = dict()
#             for key, value in kwargs.items():
#                 cls.obj[attr_contain_list_instance].update({key: value.make()})
