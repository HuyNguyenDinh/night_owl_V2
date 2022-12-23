# from tests.market.test_views import *
# from tests.market.fixtures import model_bakery_recipes
# from market.baker_recipes import *
# import time
# from django.test.testcases import TestCase
#
#
# class UserModelBakeryTest(TestCase, model_bakery_recipes.BaseModelBakeryFT):
#     @classmethod
#     def setUpClass(cls) -> None:
#         model_bakery_recipes.BaseModelBakeryFT.setUpClass(User, 'user_huy')
#         TestCase.setUpClass()
#
#     def test_get_user(self) -> None:
#         self.assertEqual(self.obj.get('user_huy'), User.objects.last())
#
#
# class UserRecipeTest(TestCase, model_bakery_recipes.BaseModelRecipeFT):
#     @classmethod
#     def setUpClass(cls) -> None:
#         model_bakery_recipes.BaseModelRecipeFT.setUpClass(user_huy, 'user_huy')
#         TestCase.setUpClass()
#
#     def first_test(self) -> None:
#         self.assertEqual(self.obj.get('user_huy'), User.objects.last())
#         self.obj['user_test'] = baker.make(User)
#
#     def second_test(self) -> None:
#         self.obj['user_normal'] = user_normal.make()
#         self.assertEqual(self.obj.get('user_normal'), User.objects.last())
#         time.sleep(60)
#
#     def test_get_user_recipe(self) -> None:
#         self.first_test()
#         self.second_test()
#
