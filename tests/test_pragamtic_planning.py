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
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
    plan = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)

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
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
    plan = PragmaticPlanning().isAchievablePlan(mpers.goals.emergencyIsDetectedGoal, fullcontext, None)

    assert True is assertPlan(
        plan, [mpers.tasks.notifyCentralBySMSTask , 
        mpers.tasks.confirmEmergencyByCallTask
        ])


def test_IsNotifiedAboutEmergency(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
    plan = PragmaticPlanning().isAchievablePlan(mpers.goals.isNotifiedAboutEmergencyGoal, fullcontext, None)

    assert True is assertPlan(
        plan, [mpers.tasks.notifyByMobileVibrationTask])

def test_centralReceivesInfo(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
    plan = PragmaticPlanning().isAchievablePlan(mpers.goals.centralReceivesInfoGoal, fullcontext, None)

    assert True is assertPlan(
        plan, [
        mpers.tasks.sendInfoByInternetTask,
        mpers.tasks.accessLocationFromTriangulationTask,
         mpers.tasks.accessDataFromDatabaseTask
        ])


def test_c1(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    plan = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    assert plan is not None

    assert False is assertPlan(
        plan, [mpers.tasks.accessLocationFromGPSTask, mpers.tasks.centralCallTask])


def test_c2(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    
    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    plan = ["acceptEmergency","notifyBySoundAlert"]
    assert tasks is not None

    for task in tasks.getTasks():
        assert task.identifier not in plan


def test_c3(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4,
                   mpers.contexts.c5, mpers.contexts.c6, mpers.contexts.c7, mpers.contexts.c8]
    
    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)

    assert tasks is not None

    for task in tasks.getTasks():
       assert task.identifier != "acceptEmergency"


def test_c4(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    plan = ["notifyCentralBySMS","confirmEmergencyByCall","notifyBySoundAlert","sendInfoBySMS","identifyLocationByVoiceCall","accessLocationFromTriangulation"]
    assert tasks is not None

    for task in tasks.getTasks():
         assert task.identifier not in plan

def test_c5(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    plan = ["notifyCentralBySMS","confirmEmergencyByCall","sendInfoBySMS","notifyBySoundAlertv"]
    assert tasks is not None

    for task in tasks.getTasks():
        assert task.identifier not in plan


def test_c6(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)

    plan = ["notifyCentralBySMS","confirmEmergencyByCall","sendInfoBySMS"]

    assert tasks is not None

    for task in tasks.getTasks():
        assert task.identifier not in plan

def test_c7(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    plan = ["notifyCentralBySMS","confirmEmergencyByCall","notifyBySoundAlert","sendInfoBySMS","identifyLocationByVoiceCall","accessLocationFromTriangulation"]
    
    assert tasks is not None
 
    for task in tasks.getTasks():
        assert task.identifier not in plan


def test_c8(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)

    plan = ["notifyCentralBySMS","confirmEmergencyByCall","notifyBySoundAlert","sendInfoBySMS","identifyLocationByVoiceCall","accessLocationFromTriangulation"]
     
    assert tasks is not None

    for task in tasks.getTasks():
        assert task.identifier not in plan


def test_c9(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c4,
                   mpers.contexts.c5, mpers.contexts.c6, mpers.contexts.c9]

    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)

    plan = ["notifyByLightAlert", "acceptEmergency"]
    assert tasks is not None
    
    for task in tasks.getTasks():
        assert task.identifier not in plan



def test_c10(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c5,
                   mpers.contexts.c6, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    plan = ["notifyByLightAlert", "acceptEmergency"]
    assert tasks is not None
    for task in tasks.getTasks():
        assert task.identifier not in plan


def test_None(mpers):
    fullcontext = []
    tasks = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)

    assert tasks is None