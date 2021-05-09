from planning.common.model.context import Context
from planning.common.model.goal import Goal
from planning.common.model.decomposition import Decomposition
from planning.common.model.task import Task
from planning.common.model.metric import Metric
from planning.common.model.quality_constraint import QualityConstraint
from planning.common.model.comparison import Comparison
from planning.common.model.interpretation import Interpretation
from tests.utils.assert_util import assertPlan
from tests.test_data.mpers_metric import MpersMetrics
from tests.test_data.mpers_knapsack_model import MpersKnapsackModel
from planning.common.model.knapsack import Knapsack
from tests.utils.assert_util import assertPlan
from planning.algorithm.pragmatic.pragmatic_planning import PragmaticPlanning
import pytest

@pytest.fixture
def mpers():
    mpers = MpersKnapsackModel()

    return mpers

def test_LocationIsIdentifiedGoal(mpers):
    fullcontext = []
    plan = PragmaticPlanning().isAchievable(mpers.goals.locationIsIdentifiedGoal, fullcontext, None)

    assert True is assertPlan(
        plan, [mpers.tasks.considerLastKnownLocationTask])
