from tests.market.fixtures.usecases.scenarios.ver1 import Fixture, Bridge
from typing import List, Dict
from typing import Iterable, Union
import itertools


class AutoCreatePropsObject(object):
    def __getattr__(self, item):
        setattr(self, item, 'N/A')


class Node(object):
    def __init__(self,
                 fixtures: AutoCreatePropsObject = AutoCreatePropsObject(),
                 bridges: AutoCreatePropsObject = AutoCreatePropsObject(),
                 currents: list[Bridge] | None = None,
                 *args, **kwargs):
        self.fixtures = fixtures
        self.bridges = bridges
        self.currents: list[Bridge] | None = currents

    def extend(self):
        temp_fixtures = AutoCreatePropsObject()
        temp_bridges = AutoCreatePropsObject()
        temp_currents = []
        for attr, value in self.fixtures.__dict__.items():
            temp_fixtures.__setattr__(attr, value.fixture_extend())
        for attr, value in self.bridges.__dict__.items():
            temp_bridges.__setattr__(attr, value.bridge_extend())
        for bridge in self.currents:
            temp_currents.append(bridge.bridge_extend())
        return Node(fixtures=temp_fixtures, bridges=temp_bridges, currents=temp_currents)

    def make(self):
        temp = []
        for bridge in self.currents:
            temp.append(bridge.bridge_extend().get_fixture())
        return temp


class Chain:
    def __init__(self,
                 fixtures: Dict[str, Fixture] | None = None,
                 bridges: Dict[str, Bridge] | None = None,
                 previous: List['Chain'] | None = None,
                 *args, **kwargs):
        self.fixtures: Dict[str, Fixture] | None = fixtures or {}
        self.bridges: Dict[str, Bridge] | None = bridges or {}
        self.previous: List['Chain'] | None = previous or []
        self._bridges: Dict[str, Bridge] = {}
        self._fixtures: Dict[str, Fixture] = {}

    def prepare_fixtures(self):
        pass

    def prepare_bridges(self):
        pass

    def prepare_previous(self):
        pass

    def get_bridge_by_name(self, bridge_name: str) -> Bridge | None:
        if self.bridges.get(bridge_name):
            return self.bridges.get(bridge_name).bridge_extend()
        return self._bridges.get(bridge_name).bridge_extend()

    def get_fixture_by_name(self, fixture_name: str) -> Fixture | None:
        if self.fixtures.get(fixture_name):
            return self.fixtures.get(fixture_name).fixture_extend()
        return self._fixtures.get(fixture_name).fixture_extend()

    def set_previous(self):
        self.previous = []
        self.prepare_previous()
        if self.previous:
            for p in self.previous:
                p.set_previous()

    def set_fixtures(self) -> Dict[str, Fixture]:
        if self.previous:
            for p in self.previous:
                temp = p.set_fixtures()
                self._fixtures = {**self._fixtures, **temp}
        self.prepare_fixtures()
        self._fixtures = {**self._fixtures, **self.fixtures}
        return self._fixtures

    def set_bridges(self) -> Dict[str, Bridge]:
        if self.previous:
            for p in self.previous:
                temp = p.set_bridges()
                self._bridges = {**self._bridges, **temp}
        self.prepare_bridges()
        self._bridges = {**self._bridges, **self.bridges}
        return self._bridges

    def extend(self) -> 'Chain':
        temp_pre: List['Chain'] = []
        temp_fixtures: Dict[str, Fixture] = {}
        temp_bridges: Dict[str, Bridge] = {}
        self.prepare_previous()
        for previous in self.previous:
            previous.prepare()
            temp_pre.append(previous.extend())
        self.prepare_fixtures()
        for key, fixture in self.fixtures.items():
            temp_fixtures[key] = fixture.fixture_extend()
        self.prepare_bridges()
        for key, bridge in self.bridges.items():
            temp_bridges[key] = bridge.bridge_extend()
        return Chain(
            fixtures=temp_fixtures,
            bridges=temp_bridges,
            previous=temp_pre
        )

    def prepare(self):
        self.set_previous()
        self.set_fixtures()
        self.set_bridges()

    def make(self):
        self.prepare()
        for _, node in self.bridges.items():
            node.bridge_extend().get_fixture()


def use_case(fixtures: Iterable[Fixture], previous_bridges: Union[Dict[str, Iterable], None] = None):
    unpack_previous_bridges = []
    result = []
    for key, value in previous_bridges.items():
        temp_for_loop = []
        for i in value:
            temp_for_loop.append((i, key))
        unpack_previous_bridges.append(temp_for_loop)
    for i in itertools.product(fixtures, *unpack_previous_bridges):
        temp_previous_bridges = {}
        for j in i:
            if isinstance(j, Fixture):
                continue
            temp_previous_bridges.update({j[1]: j[0]})
        result.append(Bridge(
            _previous=temp_previous_bridges,
            _current=i[0]
        ))
    return result
