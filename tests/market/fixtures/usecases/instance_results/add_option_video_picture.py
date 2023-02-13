from market.baker_recipes import *
from tests.market.fixtures.recipe_setups import *
from tests.market.fixtures.entities.options import *
from tests.market.fixtures.usecases.instance_results.add_options import *
from tests.market.fixtures.entities.option_pictures import *


class OptionPictureFT(AddOptionFT):
    def prepare_fixtures(self):
        super().prepare_fixtures()
        self.fixtures['option_picture_video_fixture'] = Fixture(
            _instance=Picture.recipe()
        )

    def prepare_bridges(self):
        super().prepare_bridges()
        self.bridges['full_option_picture_video'] = Bridge(
            _previous={
                'product_option': self.bridges.get('valid_product_option_full')
            },
            _current=self.fixtures.get('option_picture_video_fixture')
        )

    def get_bridge(self):
        self.bridges.get('full_option_picture_video').get_fixture()
