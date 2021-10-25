from planning.common.model.task import Task
from planning.common.model.context import Context
from planning.common.model.decomposition import Decomposition
from planning.common.model.comparison import Comparison
from planning.common.model.quality_constraint import QualityConstraint
from tests.test_data.mpers_metric import MpersMetrics
from tests.test_data.mpers_knapsack_model import MpersKnapsackModel
from planning.common.model.knapsack import Knapsack
from planning.algorithm.knapsack.knapsack_planning import KnapsackPlanning
import logging
import pytest


@pytest.fixture
def mpers():
    mpers = MpersKnapsackModel()

    return mpers

def test_getWeightWithOneMetric(mpers):
    notifyByMobileVibrationTask = mpers.tasks.notifyByMobileVibrationTask
    contexts = [None]
    result = notifyByMobileVibrationTask.getWeight(contexts)

    assert result == 2

def test_getValueWithOneMetric(mpers):
    notifyByMobileVibrationTask = mpers.tasks.notifyByMobileVibrationTask
    contexts = [None]
    result = notifyByMobileVibrationTask.getValue(contexts)

    assert result == 1/2

def test_getValueWithTwoMetrics(mpers):
    considerLastKnownLocationTask = mpers.tasks.considerLastKnownLocationTask
    contexts = [None]
    result = considerLastKnownLocationTask.getWeight(contexts)

    assert result == 915