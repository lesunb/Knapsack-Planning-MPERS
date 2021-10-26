import datetime
from planning.common.model.context import Context
from planning.common.model.goal import Goal
from planning.common.model.decomposition import Decomposition
from planning.common.model.task import Task
from planning.common.model.metric import Metric
from planning.common.model.quality_constraint import QualityConstraint
from planning.common.model.comparison import Comparison
from planning.common.model.interpretation import Interpretation
from tests.utils.assert_util import assertPlan
from tests.utils.assert_util import assertPlan2
from tests.test_data.mpers_metric import MpersMetrics
from tests.test_data.mpers_knapsack_model import MpersKnapsackModel
from planning.common.model.knapsack import Knapsack
from tests.test_data.mpers_model import MpersModel
from planning.algorithm.pragmatic.pragmatic_planning import PragmaticPlanning
from tests.utils.assert_util import assertPlan
from planning.algorithm.knapsack.knapsack_planning import KnapsackPlanning
from planning.utils.arrange_generator import ArrangeGenerator
from planning.utils.context_generator import ContextGenerator

import pytest
import logging
import datetime

log_format = '%(asctime)s: %(levelname)s: %(filename)s:'
logging.basicConfig(filemode='w+',filename='log_file.log', level=logging.DEBUG, format=log_format)

logger = logging.getLogger()


@pytest.fixture
def mpers():
    mpers = MpersModel()

    return mpers

@pytest.fixture
def mpers_knp():
    mpers_knp = MpersKnapsackModel()

    return mpers_knp


def test_planning_model(mpers,mpers_knp):

    start_time = datetime.datetime.now()
    fullcontext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4, mpers.contexts.c8]
    fullcontextKnp = [mpers_knp.contexts.c1, mpers_knp.contexts.c2, mpers_knp.contexts.c3, mpers_knp.contexts.c4, mpers_knp.contexts.c8]
    plan = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    plan2 = KnapsackPlanning().isAchievablePlan(mpers_knp.rootGoal, fullcontext, None)
    

    #assertPlan2(plan,plan2)
    #Pragmatic assert

    assert True is assertPlan2(plan,plan2)
    end_time = datetime.datetime.now()


def test_MPERS_model_Pragma(mpers_knp):
    fullcontext = [mpers_knp.contexts.c1, 
    mpers_knp.contexts.c2, mpers_knp.contexts.c3, 
    mpers_knp.contexts.c4, mpers_knp.contexts.c8]
    plan = KnapsackPlanning().isAchievablePlan(mpers_knp.rootGoal, fullcontext, None)
    #end_time = datetime.datetime.now()
    #print(end_time - start_time)
    assert True is assertPlan(
        plan, [mpers_knp.tasks.notifyCentralByInternetTask , 
        mpers_knp.tasks.confirmEmergencyByCallTask,
        mpers_knp.tasks.notifyByMobileVibrationTask,
        mpers_knp.tasks.sendInfoByInternetTask,
        mpers_knp.tasks.accessLocationFromGPSTask,
        mpers_knp.tasks.accessDataFromDatabaseTask,
        mpers_knp.tasks.ambulanceDispatchDelegationTask,
        ])

def test_MPERS_model(mpers):
    logger.warning('Iniciando teste')
    start_time = datetime.datetime.now()
    fullcontext = [mpers.contexts.c1, 
    mpers.contexts.c2, mpers.contexts.c3, 
    mpers.contexts.c4, mpers.contexts.c8]
    plan = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)
    end_time = datetime.datetime.now()
    print(end_time - start_time)
    assert True is assertPlan(
        plan, [mpers.tasks.notifyCentralBySMSTask , 
        mpers.tasks.confirmEmergencyByCallTask,
        mpers.tasks.notifyByMobileVibrationTask,
        mpers.tasks.sendInfoByInternetTask,
        mpers.tasks.accessLocationFromTriangulationTask,
        mpers.tasks.accessDataFromDatabaseTask,
        mpers.tasks.ambulanceDispatchDelegationTask,
        ])


def test_fullcontext_gen(mpers_knp,mpers):
    fullContext_knp = [mpers_knp.contexts.c1,
                mpers_knp.contexts.c2,
                mpers_knp.contexts.c3,
                mpers_knp.contexts.c4,
                mpers_knp.contexts.c5,
                mpers_knp.contexts.c6,
                mpers_knp.contexts.c7,
                mpers_knp.contexts.c8,
                mpers_knp.contexts.c9,
                mpers_knp.contexts.c10]

    fullContext_prgm = [mpers.contexts.c1,
                mpers.contexts.c2,
                mpers.contexts.c3,
                mpers.contexts.c4,
                mpers.contexts.c5,
                mpers.contexts.c6,
                mpers.contexts.c7,
                mpers.contexts.c8,
                mpers.contexts.c9,
                mpers.contexts.c10]            

    generatorKnp = ContextGenerator(fullContext_prgm)
    generatorIterKpn = iter(generatorKnp)

    lastContext = None
    numberOfContexts = 0
    diferenca = 0

    for contextKnp in generatorIterKpn:
        plan_pragma = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, contextKnp, None)
        #plan_knp = KnapsackPlanning().isAchievablePlan(mpers_knp.rootGoal, fullContext_knp, None)
        #set_knp = set(plan_knp)
        #set_prgm = set(plan_pragma)
        #dif = set_knp - set_prgm
        print("Context ", contextKnp)
        #diferenca += 1
        #registrar o diff e criar um print/log dessa diff com contador
        lastContextPrgm = contextKnp
        numberOfContexts = numberOfContexts + 1

    assert lastContextPrgm == fullContext_prgm
    assert numberOfContexts == 1024