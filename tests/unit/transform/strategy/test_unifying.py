import pytest
from unit.transform.strategy.utils.inputs import aggregator, keys
from unit.transform.strategy.utils.property_testers import ExpectedStructureProperty

from torchjd.transform.strategy import UnifyingStrategy


@pytest.mark.parametrize("strategy", [UnifyingStrategy(aggregator, key_order=keys)])
class TestUnifying(ExpectedStructureProperty):
    pass
