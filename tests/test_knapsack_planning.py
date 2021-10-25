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
import datetime
import logging
from tests.test_data.mpers_model import MpersModel
from planning.utils.arrange_generator import ArrangeGenerator
from planning.utils.context_generator import ContextGenerator

@pytest.fixture
def mpers():
    mpers = MpersKnapsackModel()

    return mpers

def test_MPERS_model(mpers):
    start_time = datetime.datetime.now()
    
    fullcontext = [mpers.contexts.c1, 
    mpers.contexts.c2, mpers.contexts.c3, 
    mpers.contexts.c4, mpers.contexts.c8]
    plan = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    end_time = datetime.datetime.now()
    print(end_time - start_time)
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
        [mpers.tasks.notifyCentralByInternetTask, 
        mpers.tasks.confirmEmergencyByCallTask])



def test_infoIsPreparedGoal(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
                
    plan = KnapsackPlanning().isAchievablePlan(mpers.goals.infoIsPreparedGoal, fullcontext, None)

    assert assertPlan(
        plan,
        [mpers.tasks.accessLocationFromGPSTask, 
        mpers.tasks.accessDataFromDatabaseTask])


def test_centralReceivesInfoGoal(mpers):
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
                
    plan = KnapsackPlanning().isAchievablePlan(mpers.goals.centralReceivesInfoGoal, fullcontext, None)

    assert assertPlan(
        plan,
        [mpers.tasks.sendInfoByInternetTask, 
        mpers.tasks.accessLocationFromGPSTask, 
        mpers.tasks.accessDataFromDatabaseTask])


def test_C1(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    plan = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    assert plan is not None

    assert False is assertPlan(
        plan, [mpers.tasks.accessLocationFromGPSTask, mpers.tasks.centralCallTask])


def test_C2(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    
    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    plan = ["acceptEmergency","notifyBySoundAlert"]
    assert tasks is not None

    for task in tasks.getTasks():
        assert task.identifier not in plan



def test_C3(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4,
                   mpers.contexts.c5, mpers.contexts.c6, mpers.contexts.c7, mpers.contexts.c8]
    
    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)


    assert tasks is not None

    for task in tasks.getTasks():
       assert task.identifier != "acceptEmergency"


def test_C4(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    plan = ["notifyCentralBySMS","confirmEmergencyByCall","notifyBySoundAlert","sendInfoBySMS","identifyLocationByVoiceCall","accessLocationFromTriangulation"]
    assert tasks is not None

    for task in tasks.getTasks():
         assert task.identifier not in plan


def test_C5(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    plan = ["notifyCentralBySMS","confirmEmergencyByCall","sendInfoBySMS","notifyBySoundAlertv"]
    assert tasks is not None

    for task in tasks.getTasks():
        assert task.identifier not in plan



def test_C6(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)


    plan = ["notifyCentralBySMS","confirmEmergencyByCall","sendInfoBySMS"]

    assert tasks is not None

    for task in tasks.getTasks():
        assert task.identifier not in plan


def test_C7(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    plan = ["notifyCentralBySMS","confirmEmergencyByCall","notifyBySoundAlert","sendInfoBySMS","identifyLocationByVoiceCall","accessLocationFromTriangulation"]
    
    assert tasks is not None
 
    for task in tasks.getTasks():
        assert task.identifier not in plan


def test_C8(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)


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


def test_C10(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c5,
                   mpers.contexts.c6, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)

    plan = ["notifyByLightAlert", "acceptEmergency"]
    assert tasks is not None
    for task in tasks.getTasks():
        assert task.identifier not in plan


#def test_None(mpers):
#    fullcontext = []
#    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)

#    assert tasks is None        

def test_C8(mpers):

    logging.info('Init planning')
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]

    tasks = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, fullContext, None)
    logging.info('Task executed')
    plan = ["notifyCentralBySMS","confirmEmergencyByCall","notifyBySoundAlert","sendInfoBySMS","identifyLocationByVoiceCall","accessLocationFromTriangulation"]
    logging.debug('a debug messag is not shown') 
    logging.info('assert')
    assert tasks is not None

    for task in tasks.getTasks():
        assert task.identifier not in plan

def test_fullContext(mpers):
    fullContext_knp = [mpers.contexts.c1,
                mpers.contexts.c2,
                mpers.contexts.c3,
                mpers.contexts.c4,
                mpers.contexts.c5,
                mpers.contexts.c6,
                mpers.contexts.c7,
                mpers.contexts.c8,
                mpers.contexts.c9,
                mpers.contexts.c10]



    generatorKnp = ContextGenerator(fullContext_knp)
    generatorIterKpn = iter(generatorKnp)

    lastContext = None
    numberOfContexts = 0
    diferenca = 0

    for contextKnp in generatorIterKpn:
        plan_knp = KnapsackPlanning().isAchievablePlan(mpers.rootGoal, contextKnp, None)
        #set_knp = set(plan_knp)
        #set_prgm = set(plan_pragma)
        #dif = set_knp - set_prgm
        #print("diferença entre os planos: ", dif)
        #diferenca += 1
        #registrar o diff e criar um print/log dessa diff com contador
        lastContextPrgm = fullContext_knp
        numberOfContexts = numberOfContexts + 1

    assert lastContextPrgm == contextKnp
    assert numberOfContexts == 1024