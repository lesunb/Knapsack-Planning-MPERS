from planning.utils.context_generator import ContextGenerator
from planning.utils.print import print_context
from tests.utils.assert_util import assertPlan
from tests.test_data.mpers_model import MpersModel
from planning.common.model.pragmatic import Pragmatic
import logging
import pytest


@pytest.fixture
def mpers():
    mpers = MpersModel()

    return mpers


def test_MPEARS(mpers):
    generator = ContextGenerator(
        [mpers.contexts.c1,
         mpers.contexts.c2,
         mpers.contexts.c3,
         mpers.contexts.c4,
         mpers.contexts.c5,
         mpers.contexts.c6,
         mpers.contexts.c7,
         mpers.contexts.c8,
         mpers.contexts.c9,
         mpers.contexts.c10,
         mpers.contexts.c12])

    generatorIter = iter(generator)

    counter = 0

    for context in generatorIter:
        counter = counter + 1
        print("INIT IN TEST FOR CONTEXT: ", counter)
        print_context(context)
        if mpers.rootGoal.isAchievable(context, None) is not None:
            print("Achievable")
            print("[")
            for task in mpers.rootGoal.isAchievable(context, None).getTasks():
                print(task.identifier + " ")

            print("]")
        else:
            print("Not achievable")

    print("END CONTADOR DE: ", counter)


def test_ContextSet1(mpers):
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

    plan = mpers.rootGoal.isAchievable(fullContext, None)

    print(plan)

    assert assertPlan(
        plan,
        [mpers.tasks.ambulanceDispatchDelegationTask,
         mpers.tasks.notifyCentralByInternetTask,
         mpers.tasks.confirmEmergencyByCallTask,
         mpers.tasks.getInfoFromResponsibleTask,
         mpers.tasks.notifyByLightAlertTask,
         mpers.tasks.sendInfoByInternetTask])


def test_contextSet1_not_found(mpers):
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

    plan = mpers.rootGoal.isAchievable(fullContext, None)

    assert plan is not None

    tasks = [mpers.tasks.notifyCentralBySMSTask,
            mpers.tasks.notifyBySoundAlertTask,
            mpers.tasks.identifyLocationByVoiceCallTask,
            mpers.tasks.accessLocationFromTriangulationTask,
            mpers.tasks.accessLocationFromGPSTask,
            mpers.tasks.considerLastKnownLocationTask,
            mpers.tasks.acceptEmergencyTask]
    
    for task in plan.getTasks():
        assert task.identifier not in tasks

def test_ContextSet2(mpers):
    fullContext = [mpers.contexts.c9,
                   mpers.contexts.c10,
                   mpers.contexts.c11]

    plan = mpers.rootGoal.isAchievable(fullContext, None)

    assert assertPlan(plan, None)


def test_ContextSet3(mpers):
    fullContext = [mpers.contexts.c4, mpers.contexts.c8, mpers.contexts.c11]

    plan = mpers.rootGoal.isAchievable(fullContext, None)

    assert assertPlan(
        plan,
        [mpers.tasks.ambulanceDispatchDelegationTask,
         mpers.tasks.acceptEmergencyTask,
         mpers.tasks.centralCallTask,
         mpers.tasks.considerLastKnownLocationTask,
         mpers.tasks.accessDataFromDatabaseTask,
         mpers.tasks.sendInfoByInternetTask,
         mpers.tasks.notifyCentralByInternetTask])


def test_contextSet3_not_found(mpers):
    fullContext = [mpers.contexts.c4, mpers.contexts.c8, mpers.contexts.c11]

    plan = mpers.rootGoal.isAchievable(fullContext, None)

    assert plan is not None

    tasks = [mpers.tasks.confirmEmergencyByCallTask,
            mpers.tasks.notifyCentralBySMSTask,
            mpers.tasks.getInfoFromResponsibleTask,
            mpers.tasks.notifyBySoundAlertTask,
            mpers.tasks.notifyByLightAlertTask,
            mpers.tasks.notifyByMobileVibrationTask,
            mpers.tasks.sendInfoBySMSTask]
    
    for task in plan.getTasks():
        assert task.identifier not in tasks



def test_ContextSet4(mpers):
    fullContext = [mpers.contexts.c1,
                   mpers.contexts.c2,
                   mpers.contexts.c3,
                   mpers.contexts.c6,
                   mpers.contexts.c7]

    plan = mpers.rootGoal.isAchievable(fullContext, None)

    assert assertPlan(
        plan,
        [mpers.tasks.accessLocationFromTriangulationTask,
         mpers.tasks.notifyByLightAlertTask,
         mpers.tasks.confirmEmergencyByCallTask,
         mpers.tasks.notifyCentralBySMSTask,
         mpers.tasks.sendInfoByInternetTask,
         mpers.tasks.accessDataFromDatabaseTask,
         mpers.tasks.ambulanceDispatchDelegationTask])


def test_contextSet4_not_found(mpers):
    fullContext = [mpers.contexts.c1,
                   mpers.contexts.c2,
                   mpers.contexts.c3,
                   mpers.contexts.c6,
                   mpers.contexts.c7]

    plan = mpers.rootGoal.isAchievable(fullContext, None)

    assert plan is not None

    tasks = [mpers.tasks.acceptEmergencyTask,
            mpers.tasks.centralCallTask,
            mpers.tasks.accessLocationFromGPSTask]
    
    for task in plan.getTasks():
        assert task.identifier not in tasks
