from planning.common.model.knapsack_object import KnapsackObject
from planning.common.model.task import Task
from planning.common.model.context import Context
from planning.common.model.decomposition import Decomposition
from planning.common.model.comparison import Comparison
from planning.common.model.quality_constraint import QualityConstraint
from tests.test_data.mpers_metric import MpersMetrics
from tests.test_data.mpers_knapsack_model import MpersKnapsackModel
from planning.common.model.knapsack import Knapsack
from planning.algorithm.knapsack.knapsack_planning import KnapsackPlanning

import pytest


@pytest.fixture
def mpers():
    mpers = MpersKnapsackModel()

    return mpers


def test_shouldProvideCorrectValueForMetric():
    task = KnapsackObject("T1")
    currentContext = Context("C1")
    fullContext = []

    fullContext.append(currentContext)

    task.setProvidedQuality(currentContext, MpersMetrics.METERS, 30)

    assert 30 == task.myProvidedQuality(MpersMetrics.METERS, fullContext)


def test_shouldProvideMetricForBaseline():
    task = KnapsackObject("t1")

    current = Context("C1")
    fullContext = []
    fullContext.append(current)

    task.setProvidedQuality(None, MpersMetrics.METERS, 30.0)

    assert 30.0 ==task.myProvidedQuality(MpersMetrics.METERS, fullContext)


def test_metricNotFound():
    task = KnapsackObject("T1")
    currentContext = Context("C1")
    fullContext = []

    fullContext.append(currentContext)

    task.setProvidedQuality(currentContext, MpersMetrics.METERS, 30.0)

    result = task.myProvidedQuality(MpersMetrics.SECONDS, fullContext)
    assert result is None


def test_metricNotFound():
    task = KnapsackObject("T1")
    currentContext = Context("C1")
    fullContext = []

    fullContext.append(currentContext)

    task.setProvidedQuality(currentContext, MpersMetrics.METERS, 30.0)

    result = task.myProvidedQuality(MpersMetrics.SECONDS, fullContext)
    assert result is None


def test_OnlyBaselineDefined():
    task = KnapsackObject("T1")
    baseline = Context(None)
    fullContext = []

    fullContext.append(baseline)

    task.setProvidedQuality(baseline, MpersMetrics.METERS, 50.0)

    assert 50.0 == task.myProvidedQuality(MpersMetrics.METERS, fullContext)


def test_shouldProvideSpecificContextMetric():
    task = KnapsackObject("T2")
    currentContext = Context("C1")
    baseline = None
    fullContext = []

    fullContext.append(currentContext)
    fullContext.append(baseline)

    task.setProvidedQuality(currentContext, MpersMetrics.METERS, 50)
    task.setProvidedQuality(baseline, MpersMetrics.METERS, 30)

    assert 50 == task.myProvidedQuality(MpersMetrics.METERS, fullContext)


def test_abidesByInterpretation_passing_baseline(mpers):
    isNotifiedAboutEmergencyGoal = mpers.goals.isNotifiedAboutEmergencyGoal
    notifyByMobileVibrationTask = mpers.tasks.notifyByMobileVibrationTask
    c1 = mpers.contexts.c1
    c9 = mpers.contexts.c9

    context = [c1]
    result = KnapsackPlanning().abidesByInterpretation(notifyByMobileVibrationTask, 
        isNotifiedAboutEmergencyGoal.interp, context)
    assert result == True

    context = [c9]
    result = KnapsackPlanning().abidesByInterpretation(notifyByMobileVibrationTask, 
        isNotifiedAboutEmergencyGoal.interp, context)
    assert result == True


def test_abidesByInterpretation_not_passing_baseline(mpers):
    isNotifiedAboutEmergencyGoal = mpers.goals.isNotifiedAboutEmergencyGoal
    notifyBySoundAlertTask = mpers.tasks.notifyBySoundAlertTask
    c6 = mpers.contexts.c6
    c1 = mpers.contexts.c1

    context = [c6]
    result = KnapsackPlanning().abidesByInterpretation(notifyBySoundAlertTask, 
        isNotifiedAboutEmergencyGoal.interp, context)
    assert result == True

    context = [c1]
    result = KnapsackPlanning().abidesByInterpretation(notifyBySoundAlertTask, 
        isNotifiedAboutEmergencyGoal.interp, context)
    assert result == False


def test_abidesByInterpretation_only_baseline(mpers):
    considerLastKnownLocationTask = mpers.tasks.considerLastKnownLocationTask
    locationIsIdentifiedGoal = mpers.goals.locationIsIdentifiedGoal
    context = []

    result = KnapsackPlanning().abidesByInterpretation(considerLastKnownLocationTask, 
        locationIsIdentifiedGoal.interp, context)
    assert result == True


def test_abidesByInterpretation_only_baseline_context(mpers):
    considerLastKnownLocationTask = mpers.tasks.considerLastKnownLocationTask
    locationIsIdentifiedGoal = mpers.goals.locationIsIdentifiedGoal
    c1 = mpers.contexts.c1
    c2 = mpers.contexts.c2
    c3 = mpers.contexts.c3

    context = [c1, c2, c3]

    result = KnapsackPlanning().abidesByInterpretation(considerLastKnownLocationTask, 
        locationIsIdentifiedGoal.interp, context)
    assert result == True


def test_abidesByInterpretation_context_not_passing(mpers):
    identifyLocationByVoiceCallTask = mpers.tasks.identifyLocationByVoiceCallTask
    locationIsIdentifiedGoal = mpers.goals.locationIsIdentifiedGoal
    c5 = mpers.contexts.c5

    context = []

    result = KnapsackPlanning().abidesByInterpretation(identifyLocationByVoiceCallTask, 
        locationIsIdentifiedGoal.interp, context)
    assert result == True

    context.append(c5)

    result = KnapsackPlanning().abidesByInterpretation(identifyLocationByVoiceCallTask, 
        locationIsIdentifiedGoal.interp, context)
    assert result == False


def test_abidesByInterpretation_only_baseline_not_passing(mpers):
    locationIsIdentifiedGoal = mpers.goals.locationIsIdentifiedGoal
    context = []

    LongSecondsTask = KnapsackObject("LongSecondsTask")
    LongSecondsTask.setProvidedQuality(
        None, MpersMetrics.SECONDS, 1500)

    result = KnapsackPlanning().abidesByInterpretation(LongSecondsTask, 
        locationIsIdentifiedGoal.interp, context)
    assert result == False


def test_myQualityBaseline(mpers):
    accessLocationFromTriangulationTask = mpers.tasks.accessLocationFromTriangulationTask
    c2 = mpers.contexts.c2
    c11 = mpers.contexts.c11

    context = [c2]
    result = accessLocationFromTriangulationTask.myProvidedQuality(MpersMetrics.DISTANCE_ERROR, context)
    assert result == 40

    context.append(c11)
    result = accessLocationFromTriangulationTask.myProvidedQuality(MpersMetrics.DISTANCE_ERROR, context)
    assert result == 400
