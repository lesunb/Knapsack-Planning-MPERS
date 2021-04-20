from planning.common.model.context import Context
from planning.common.model.pragmatic import Pragmatic
from planning.common.model.goal import Goal
from planning.common.model.decomposition import Decomposition
from planning.common.model.task import Task
from planning.common.model.metric import Metric
from planning.common.model.quality_constraint import QualityConstraint
from planning.common.model.comparison import Comparison
from planning.common.model.interpretation import Interpretation
from tests.utils.assert_util import assertPlan
from tests.test_data.mpers_metric import MpersMetrics
from tests.test_data.mpers_model import MpersModel
from planning.algorithm.pragmatic.pragmatic_planning import PragmaticPlanning
import pytest


@pytest.fixture
def mpers():
    mpers = MpersModel()

    return mpers

def test_MPERS_model(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
    plan = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    assert True is assertPlan(
        plan, [mpers.tasks.notifyCentralBySMSTask , 
        mpers.tasks.confirmEmergencyByCallTask,
        mpers.tasks.notifyByMobileVibrationTask,
        mpers.tasks.sendInfoByInternetTask,
        mpers.tasks.accessLocationFromTriangulationTask,
        mpers.tasks.accessDataFromDatabaseTask,
        mpers.tasks.ambulanceDispatchDelegationTask,
        ])

    
def test_EmergencyIsDetected(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
    plan = PragmaticPlanning().isAchievablePlan(mpers.goals.emergencyIsDetectedGoal, fullContext, None)

    assert True is assertPlan(
        plan, [mpers.tasks.notifyCentralBySMSTask , 
        mpers.tasks.confirmEmergencyByCallTask
        ])


def test_IsNotifiedAboutEmergency(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
    plan = PragmaticPlanning().isAchievablePlan(mpers.goals.isNotifiedAboutEmergencyGoal, fullContext, None)

    assert True is assertPlan(
        plan, [mpers.tasks.notifyByMobileVibrationTask])

def test_centralReceivesInfo(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
    plan = PragmaticPlanning().isAchievablePlan(mpers.goals.centralReceivesInfoGoal, fullContext, None)

    assert True is assertPlan(
        plan, [
        mpers.tasks.sendInfoByInternetTask,
        mpers.tasks.accessLocationFromTriangulationTask,
         mpers.tasks.accessDataFromDatabaseTask
        ])


def test_C1(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    plan = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)
    assert plan is not None

    assert False is assertPlan(
        plan, [mpers.tasks.accessLocationFromGPSTask, mpers.tasks.centralCallTask])


def test_C2(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    
    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    assert tasks is not None

    for task in tasks.getTasks():
        found = 0

        if task.identifier == "acceptEmergency":
            found = 1
        if task.identifier == "notifyBySoundAlert":
            found = 1

        assert found == 0


def test_C3(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4,
                   mpers.contexts.c5, mpers.contexts.c6, mpers.contexts.c7, mpers.contexts.c8]
    
    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    assert tasks is not None

    for task in tasks.getTasks():
        found = 0

        if task.identifier == "acceptEmergency":
            found = 1

        assert found == 0


def test_C4(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    assert tasks is not None

    for task in tasks.getTasks():
        found = 0

        if task.identifier == "notifyCentralBySMS":
            found = 1
        if task.identifier == "confirmEmergencyByCall":
            found = 1
        if task.identifier == "notifyBySoundAlert":
            found = 1
        if task.identifier == "sendInfoBySMS":
            found = 1
        if task.identifier == "identifyLocationByVoiceCall":
            found = 1
        if task.identifier == "accessLocationFromTriangulation":
            found = 1

        assert found == 0


def test_C5(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    assert tasks is not None

    for task in tasks.getTasks():
        found = 0

        if task.identifier == "notifyCentralBySMS":
            found = 1
        if task.identifier == "notifyBySoundAlert":
            found = 1
        if task.identifier == "sendInfoBySMS":
            found = 1
        if task.identifier == "confirmEmergencyByCall":
            found = 1

        assert found == 0


def test_C6(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    assert tasks is not None

    for task in tasks.getTasks():
        found = 0

        if task.identifier == "notifyCentralBySMS":
            found = 1
        if task.identifier == "sendInfoBySMS":
            found = 1
        if task.identifier == "confirmEmergencyByCall":
            found = 1

        assert found == 0


def test_C7(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    assert tasks is not None

    for task in tasks.getTasks():
        found = 0

        if task.identifier == "notifyCentralBySMS":
            found = 1
        if task.identifier == "confirmEmergencyByCall":
            found = 1
        if task.identifier == "notifyBySoundAlert":
            found = 1
        if task.identifier == "sendInfoBySMS":
            found = 1
        if task.identifier == "identifyLocationByVoiceCall":
            found = 1
        if task.identifier == "accessLocationFromTriangulation":
            found = 1
        if task.identifier == "accessLocationFromGPS":
            found = 1

        assert found == 0


def test_C8(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    assert tasks is not None

    for task in tasks.getTasks():
        found = 0

        if task.identifier == "notifyCentralBySMS":
            found = 1
        if task.identifier == "confirmEmergencyByCall":
            found = 1
        if task.identifier == "notifyBySoundAlert":
            found = 1
        if task.identifier == "sendInfoBySMS":
            found = 1
        if task.identifier == "identifyLocationByVoiceCall":
            found = 1
        if task.identifier == "accessLocationFromTriangulation":
            found = 1

        assert found == 0


def test_C9(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c4,
                   mpers.contexts.c5, mpers.contexts.c6, mpers.contexts.c9]

    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    assert tasks is not None

    for task in tasks.getTasks():
        found = 0

        if task.identifier == "notifyByLightAlert":
            found = 1
        if task.identifier == "acceptsEmergency":
            found = 1

        assert found == 0



def test_C10(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c5,
                   mpers.contexts.c6, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    assert tasks is not None
    for task in tasks.getTasks():
        found = 0

        if task.identifier == "notifyByLightAlert":
            found = 1
        if task.identifier == "acceptEmergency":
            found = 1

        assert found == 0


def test_None(mpers):
    fullContext = []
    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    assert tasks is None
