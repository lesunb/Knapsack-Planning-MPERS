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
from planning.algorithm.knapsack.knapsack_planning import KnapsackPlanning

import pytest


@pytest.fixture
def mpers():
    mpers = MpersKnapsackModel()

    return mpers

def test_IsNotifiedAboutEmergencyGoal(mpers):
    fullContext = [mpers.contexts.c1,
                mpers.contexts.c2,
                mpers.contexts.c3,
                mpers.contexts.c4,
                mpers.contexts.c5,
                mpers.contexts.c6,
                mpers.contexts.c7,
                mpers.contexts.c8,
                mpers.contexts.c9,
                mpers.contexts.c10]
                
    plan = KnapsackPlanning().isAchievablePlan(mpers.goals.isNotifiedAboutEmergencyGoal, fullContext, None)

    assert assertPlan(
        plan,
        [mpers.tasks.notifyByLightAlertTask])

def test_EmergencyIsDetectedGoal(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
    plan = KnapsackPlanning().isAchievablePlan(mpers.goals.emergencyIsDetectedGoal, fullContext, None)

    assert assertPlan(
        plan,
        [mpers.tasks.notifyCentralByInternetTask, mpers.tasks.confirmEmergencyByCallTask])



def infoIsPreparedGoal(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
                
    plan = KnapsackPlanning().isAchievablePlan(mpers.goals.infoIsPreparedGoal, fullContext, None)

    assert assertPlan(
        plan,
        [mpers.tasks.accessLocationFromGPSTask, mpers.tasks.accessDataFromDatabaseTask])


def centralReceivesInfoGoal(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
                
    plan = KnapsackPlanning().isAchievablePlan(mpers.goals.centralReceivesInfoGoal, fullContext, None)

    assert assertPlan(
        plan,
        [mpers.tasks.sendInfoByInternetTask, mpers.tasks.accessLocationFromGPSTask, mpers.tasks.accessDataFromDatabaseTask])

