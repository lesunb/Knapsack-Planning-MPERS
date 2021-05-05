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

def test_MPERS_model(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
    plan = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)

    assert True is assertPlan(
        plan, [mpers.tasks.notifyCentralByInternetTask , 
        mpers.tasks.confirmEmergencyByCallTask,
        mpers.tasks.notifyByMobileVibrationTask,
        mpers.tasks.sendInfoByInternetTask,
        mpers.tasks.accessLocationFromGPSTask,
        mpers.tasks.accessDataFromDatabaseTask,
        mpers.tasks.ambulanceDispatchDelegationTask,
        ])

def test_IsNotifiedAboutEmergencyGoal(mpers):
    fullcontext = [mpers.contexts.c1,
                mpers.contexts.c2,
                mpers.contexts.c3,
                mpers.contexts.c4,
                mpers.contexts.c5,
                mpers.contexts.c6,
                mpers.contexts.c7,
                mpers.contexts.c8,
                mpers.contexts.c9,
                mpers.contexts.c10]
                
    plan = KnapsackPlanning().isAchievablePlan(mpers.goals.isNotifiedAboutEmergencyGoal, fullcontext, None)

    assert assertPlan(
        plan,
        [mpers.tasks.notifyByLightAlertTask])

def test_EmergencyIsDetectedGoal(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
    plan = KnapsackPlanning().isAchievablePlan(mpers.goals.emergencyIsDetectedGoal, fullcontext, None)

    assert assertPlan(
        plan,
        [mpers.tasks.notifyCentralByInternetTask, mpers.tasks.confirmEmergencyByCallTask])



def test_infoIsPreparedGoal(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
                
    plan = KnapsackPlanning().isAchievablePlan(mpers.goals.infoIsPreparedGoal, fullcontext, None)

    assert assertPlan(
        plan,
        [mpers.tasks.accessLocationFromGPSTask, mpers.tasks.accessDataFromDatabaseTask])


def test_centralReceivesInfoGoal(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
                
    plan = KnapsackPlanning().isAchievablePlan(mpers.goals.centralReceivesInfoGoal, fullcontext, None)

    assert assertPlan(
        plan,
        [mpers.tasks.sendInfoByInternetTask, mpers.tasks.accessLocationFromGPSTask, mpers.tasks.accessDataFromDatabaseTask])

def test_c1(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    plan = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    assert plan is not None

    assert False is assertPlan(
        plan, [mpers.tasks.accessLocationFromGPSTask, mpers.tasks.centralCallTask])

def test_c2(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    
    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    plan = ["acceptEmergency","notifyBySoundAlert"]
    assert tasks is not None

    for task in tasks.getTasks():
        assert task.identifier not in plan


def test_c3(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4,
                   mpers.contexts.c5, mpers.contexts.c6, mpers.contexts.c7, mpers.contexts.c8]
    
    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)

    assert tasks is not None

    for task in tasks.getTasks():
       assert task.identifier != "acceptEmergency"


def test_c4(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    plan = ["notifyCentralBySMS","confirmEmergencyByCall","notifyBySoundAlert","sendInfoBySMS","identifyLocationByVoiceCall","accessLocationFromTriangulation"]
    assert tasks is not None

    for task in tasks.getTasks():
         assert task.identifier not in plan

def test_c5(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    plan = ["notifyCentralBySMS","confirmEmergencyByCall","sendInfoBySMS","notifyBySoundAlertv"]
    assert tasks is not None

    for task in tasks.getTasks():
        assert task.identifier not in plan


def test_c6(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)

    plan = ["notifyCentralBySMS","confirmEmergencyByCall","sendInfoBySMS"]

    assert tasks is not None

    for task in tasks.getTasks():
        assert task.identifier not in plan

def test_c7(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    plan = ["notifyCentralBySMS","confirmEmergencyByCall","notifyBySoundAlert","sendInfoBySMS","identifyLocationByVoiceCall","accessLocationFromTriangulation"]
    
    assert tasks is not None
 
    for task in tasks.getTasks():
        assert task.identifier not in plan


def test_c8(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)

    plan = ["notifyCentralBySMS","confirmEmergencyByCall","notifyBySoundAlert","sendInfoBySMS","identifyLocationByVoiceCall","accessLocationFromTriangulation"]
     
    assert tasks is not None

    for task in tasks.getTasks():
        assert task.identifier not in plan


def test_c9(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c4,
                   mpers.contexts.c5, mpers.contexts.c6, mpers.contexts.c9]

    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)

    plan = ["notifyByLightAlert", "acceptEmergency"]
    assert tasks is not None
    
    for task in tasks.getTasks():
        assert task.identifier not in plan


def test_c10(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c5,
                   mpers.contexts.c6, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    plan = ["notifyByLightAlert", "acceptEmergency"]
    assert tasks is not None
    for task in tasks.getTasks():
        assert task.identifier not in plan


def test_None(mpers):
    fullcontext = []
    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)

    assert tasks is None        