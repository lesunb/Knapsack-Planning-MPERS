from planning.common.model.context import Context
from planning.common.model.knapsack import Knapsack
from planning.common.model.knapsack_object import KnapsackObject
from planning.common.model.goal import Goal
from planning.common.model.decomposition import Decomposition
from planning.common.model.task import Task
from planning.common.model.quality_constraint import QualityConstraint
from planning.common.model.comparison import Comparison
from tests.test_data.mpers_metric import MpersMetrics


class MpersKnapsackContexts():

    # Contexts
    c1 = Context("c1")
    c2 = Context("c2")
    c3 = Context("c3")
    c4 = Context("c4")
    c5 = Context("c5")
    c6 = Context("c6")
    c7 = Context("c7")
    c8 = Context("c8")
    c9 = Context("c9")
    c10 = Context("c10")
    c11 = Context("c11")
    c12 = Context("c12")

class MpersKnapsackTasks():
    def __init__(self):

        # Tasks
        self.notifyCentralBySMSTask = KnapsackObject("notifyCentralBySMSTask")
        self.notifyCentralByInternetTask = KnapsackObject("notifyCentralByInternetTask")
        self.acceptEmergencyTask = KnapsackObject("acceptEmergencyTask")
        self.confirmEmergencyByCallTask = KnapsackObject("confirmEmergencyByCallTask")
        self.processDataFromSensorsTask = KnapsackObject("processDataFromSensorsTask")
        self.identifySituationTask = KnapsackObject("identifySituationTask")
        self.collectDataFromSensorsTask = KnapsackObject("collectDataFromSensorsTask")
        self.persistDataToDatabaseTask = KnapsackObject("persistDataToDatabaseTask")
        self.notifyByMobileVibrationTask = KnapsackObject("notifyByMobileVibrationTask")
        self.notifyBySoundAlertTask = KnapsackObject("notifyBySoundAlertTask")
        self.notifyByLightAlertTask = KnapsackObject("notifyByLightAlertTask")
        self.centralCallTask = KnapsackObject("centralCallsPTask")
        self.sendInfoBySMSTask = KnapsackObject("sendInfoBySMSTask")
        self.sendInfoByInternetTask = KnapsackObject("sendInfoByInternetTask")
        self.considerLastKnownLocationTask = KnapsackObject(
            "considerLastKnownLocationTask")
        self.identifyLocationByVoiceCallTask = KnapsackObject(
            "identifyLocationByVoiceCallTask")
        self.accessLocationFromTriangulationTask = KnapsackObject(
            "accessLocationFromTriangulationTask")
        self.accessLocationFromGPSTask = KnapsackObject("accessLocationFromGPSTask")
        self.accessDataFromDatabaseTask = KnapsackObject("accessDataFromDatabaseTask")
        self.getInfoFromResponsibleTask = KnapsackObject("getInfoFromResponsibleTask")
        self.ambulanceDispatchDelegationTask = KnapsackObject(
            "ambulanceDispatchDelegationTask")


class MpersKnapsackGoals():

    def __init__(self):
        # Goals
        self.respondToEmergencyGoal = Knapsack(
            Decomposition.AND, "respondToEmergencyGoal")
        self.emergencyIsDetectedGoal = Knapsack(
            Decomposition.OR, "emergencyIsDetectedGoal")
        self.centralReceivesInfoGoal = Knapsack(
            Decomposition.AND, "centralReceivesInfoGoal")
        self.locationIsIdentifiedGoal = Knapsack(
            Decomposition.OR, "locationIsIdentifiedGoal")
        self.infoIsPreparedGoal = Knapsack(
            Decomposition.OR, "infoIsPreparedGoal")
        self.isNotifiedAboutEmergencyGoal = Knapsack(
            Decomposition.OR, "isNotifiedAboutEmergencyGoal")
        self.callForHelpIsAcceptedGoal = Knapsack(
            Decomposition.AND, "callForHelpIsAcceptedGoal")
        self.falseAlarmIsCheckedGoal = Knapsack(
            Decomposition.OR, "falseAlarmIsCheckedGoal")
        self.receivesEmergencyButtonCallGoal = Knapsack(
            Decomposition.OR, "receivesEmergencyButtonCallGoal")
        self.situationsAreIdentifiedGoal = Knapsack(
            Decomposition.AND, "situationsAreIdentifiedGoal")
        self.infoIsSentToEmergencyGoal = Knapsack(
            Decomposition.OR, "infoIsSentToEmergencyGoal")
        self.setupAutomatedInfoGoal = Knapsack(
            Decomposition.AND, "setupAutomatedInfoGoal")
        self.situationDataIsRecoveredGoal = Knapsack(
            Decomposition.AND, "situationDataIsRecoveredGoal")
        self.contactResponsibleGoal = Knapsack(
            Decomposition.AND, "contactResponsibleGoal")
        self.medicalCareReachesGoal = Knapsack(
            Decomposition.AND, "medicalCareReachesGoal")
        self.ambulanceIsDispatchedToLocationGoal = Knapsack(
            Decomposition.AND, "ambulanceIsDispatchedToLocationGoal")


class MpersKnapsackModel():
 
    contexts = MpersKnapsackContexts()

    def __init__(self):

        self.tasks = MpersKnapsackTasks()
        self.goals = MpersKnapsackGoals()

        # Refinements

        self.goals.respondToEmergencyGoal.addDependency(
            self.goals.emergencyIsDetectedGoal)
        self.goals.respondToEmergencyGoal.addDependency(
            self.goals.isNotifiedAboutEmergencyGoal)
        self.goals.respondToEmergencyGoal.addDependency(
            self.goals.centralReceivesInfoGoal)
        self.goals.respondToEmergencyGoal.addDependency(
            self.goals.medicalCareReachesGoal)

        self.goals.emergencyIsDetectedGoal.addDependency(
            self.goals.callForHelpIsAcceptedGoal)
        self.goals.emergencyIsDetectedGoal.addDependency(
            self.goals.situationsAreIdentifiedGoal)

        self.goals.callForHelpIsAcceptedGoal.addDependency(
            self.goals.receivesEmergencyButtonCallGoal)
        self.goals.callForHelpIsAcceptedGoal.addDependency(
            self.goals.falseAlarmIsCheckedGoal)

        self.goals.receivesEmergencyButtonCallGoal.addDependency(
            self.tasks.notifyCentralBySMSTask)
        self.goals.receivesEmergencyButtonCallGoal.addDependency(
            self.tasks.notifyCentralByInternetTask)

        self.goals.falseAlarmIsCheckedGoal.addDependency(
            self.tasks.acceptEmergencyTask)
        self.goals.falseAlarmIsCheckedGoal.addDependency(
            self.tasks.confirmEmergencyByCallTask)

        self.goals.situationsAreIdentifiedGoal.addDependency(
            self.tasks.processDataFromSensorsTask)
        self.goals.situationsAreIdentifiedGoal.addDependency(
            self.tasks.identifySituationTask)

        self.goals.situationsAreIdentifiedGoal.addDependency(
            self.tasks.collectDataFromSensorsTask)
        self.goals.situationsAreIdentifiedGoal.addDependency(
            self.tasks.persistDataToDatabaseTask)

        self.goals.isNotifiedAboutEmergencyGoal.addDependency(
            self.tasks.notifyByLightAlertTask)
        self.goals.isNotifiedAboutEmergencyGoal.addDependency(
            self.tasks.notifyByMobileVibrationTask)
        self.goals.isNotifiedAboutEmergencyGoal.addDependency(
            self.tasks.notifyBySoundAlertTask)
        self.goals.isNotifiedAboutEmergencyGoal.addDependency(
            self.tasks.centralCallTask)

        self.goals.centralReceivesInfoGoal.addDependency(
            self.goals.infoIsSentToEmergencyGoal)
        self.goals.centralReceivesInfoGoal.addDependency(
            self.goals.infoIsPreparedGoal)

        self.goals.infoIsSentToEmergencyGoal.addDependency(
            self.tasks.sendInfoByInternetTask)
        self.goals.infoIsSentToEmergencyGoal.addDependency(
            self.tasks.sendInfoBySMSTask)
            
        self.goals.infoIsPreparedGoal.addDependency(
            self.goals.setupAutomatedInfoGoal)
        self.goals.infoIsPreparedGoal.addDependency(
            self.goals.contactResponsibleGoal)

        self.goals.setupAutomatedInfoGoal.addDependency(
            self.goals.locationIsIdentifiedGoal)
        self.goals.setupAutomatedInfoGoal.addDependency(
            self.goals.situationDataIsRecoveredGoal)

        self.goals.locationIsIdentifiedGoal.addDependency(
            self.tasks.accessLocationFromTriangulationTask)
        self.goals.locationIsIdentifiedGoal.addDependency(
            self.tasks.considerLastKnownLocationTask)
        self.goals.locationIsIdentifiedGoal.addDependency(
            self.tasks.identifyLocationByVoiceCallTask)
        self.goals.locationIsIdentifiedGoal.addDependency(
            self.tasks.accessLocationFromGPSTask)

        self.goals.situationDataIsRecoveredGoal.addDependency(
            self.tasks.accessDataFromDatabaseTask)

        self.goals.contactResponsibleGoal.addDependency(
            self.tasks.getInfoFromResponsibleTask)

        self.goals.medicalCareReachesGoal.addDependency(
            self.goals.ambulanceIsDispatchedToLocationGoal)

        self.goals.ambulanceIsDispatchedToLocationGoal.addDependency(
            self.tasks.ambulanceDispatchDelegationTask)

        # Applicable Contexts

        self.tasks.notifyCentralBySMSTask.addApplicableContext(
            self.contexts.c2)

        self.tasks.notifyCentralByInternetTask.addApplicableContext(
            self.contexts.c3)
        self.tasks.notifyCentralByInternetTask.addApplicableContext(
            self.contexts.c4)

        self.tasks.acceptEmergencyTask.addNonapplicableContext(
            self.contexts.c2)

        self.tasks.confirmEmergencyByCallTask.addApplicableContext(
            self.contexts.c2)

        self.tasks.notifyByMobileVibrationTask.addApplicableContext(
            self.contexts.c1)

        self.tasks.notifyBySoundAlertTask.addApplicableContext(
            self.contexts.c6)

        self.tasks.notifyByLightAlertTask.addApplicableContext(
            self.contexts.c7)

        self.tasks.centralCallTask.addApplicableContext(self.contexts.c8)

        self.tasks.sendInfoBySMSTask.addApplicableContext(self.contexts.c2)

        self.tasks.sendInfoByInternetTask.addApplicableContext(
            self.contexts.c3)
        self.tasks.sendInfoByInternetTask.addApplicableContext(
            self.contexts.c4)

        self.tasks.identifyLocationByVoiceCallTask.addApplicableContext(
            self.contexts.c2)

        self.tasks.accessLocationFromTriangulationTask.addApplicableContext(
            self.contexts.c2)


        # Goal Interpretation

        qc1 = QualityConstraint(None, MpersMetrics.SECONDS, 180,
                                Comparison.LESS_OR_EQUAL_TO)
        qc2 = QualityConstraint(self.contexts.c10, MpersMetrics.SECONDS, 90,
                                Comparison.LESS_OR_EQUAL_TO)
        qc3 = QualityConstraint(self.contexts.c9, MpersMetrics.SECONDS, 240,
                                Comparison.LESS_OR_EQUAL_TO)
        self.goals.respondToEmergencyGoal.interp.addQualityConstraint(qc1)
        self.goals.respondToEmergencyGoal.interp.addQualityConstraint(qc2)
        self.goals.respondToEmergencyGoal.interp.addQualityConstraint(qc3)

        qc1 = QualityConstraint(
            None, MpersMetrics.FALSE_NEGATIVE_PERCENTAGE, 30, Comparison.LESS_OR_EQUAL_TO)
        qc2 = QualityConstraint(
            self.contexts.c3, MpersMetrics.FALSE_NEGATIVE_PERCENTAGE, 10, Comparison.LESS_OR_EQUAL_TO)
        qc3 = QualityConstraint(
            self.contexts.c9, MpersMetrics.FALSE_NEGATIVE_PERCENTAGE, 5, Comparison.LESS_OR_EQUAL_TO)
        self.goals.emergencyIsDetectedGoal.interp.addQualityConstraint(qc1)
        self.goals.emergencyIsDetectedGoal.interp.addQualityConstraint(qc2)
        self.goals.emergencyIsDetectedGoal.interp.addQualityConstraint(qc3)

        qc1 = QualityConstraint(None, MpersMetrics.SECONDS, 60,
                                Comparison.LESS_OR_EQUAL_TO)
        self.goals.centralReceivesInfoGoal.interp.addQualityConstraint(qc1)

        qc4 = QualityConstraint(None, MpersMetrics.DISTANCE_ERROR, 1000,
                                Comparison.LESS_OR_EQUAL_TO)
        qc6 = QualityConstraint(self.contexts.c5, MpersMetrics.DISTANCE_ERROR,
                                20, Comparison.LESS_OR_EQUAL_TO)
        qc5 = QualityConstraint(self.contexts.c10, MpersMetrics.DISTANCE_ERROR,
                                200, Comparison.LESS_OR_EQUAL_TO)
        qc1 = QualityConstraint(None, MpersMetrics.SECONDS, 120,
                                Comparison.LESS_OR_EQUAL_TO)
        qc3 = QualityConstraint(self.contexts.c9, MpersMetrics.SECONDS, 240,
                                Comparison.LESS_OR_EQUAL_TO)
        qc2 = QualityConstraint(self.contexts.c10, MpersMetrics.SECONDS, 20,
                                Comparison.LESS_OR_EQUAL_TO)
        self.goals.locationIsIdentifiedGoal.interp.addQualityConstraint(qc1)
        self.goals.locationIsIdentifiedGoal.interp.addQualityConstraint(qc2)
        self.goals.locationIsIdentifiedGoal.interp.addQualityConstraint(qc3)
        self.goals.locationIsIdentifiedGoal.interp.addQualityConstraint(qc4)
        self.goals.locationIsIdentifiedGoal.interp.addQualityConstraint(qc5)
        self.goals.locationIsIdentifiedGoal.interp.addQualityConstraint(qc6)

        qc1 = QualityConstraint(None, MpersMetrics.SECONDS, 45,
                                Comparison.LESS_OR_EQUAL_TO)
        qc2 = QualityConstraint(self.contexts.c10, MpersMetrics.SECONDS, 30,
                                Comparison.LESS_OR_EQUAL_TO)
        self.goals.infoIsPreparedGoal.interp.addQualityConstraint(qc1)
        self.goals.infoIsPreparedGoal.interp.addQualityConstraint(qc2)

        qc1 = QualityConstraint(None, MpersMetrics.NOISE, 10,
                                Comparison.LESS_OR_EQUAL_TO)
        qc2 = QualityConstraint(self.contexts.c1, MpersMetrics.NOISE, 3,
                                Comparison.LESS_OR_EQUAL_TO)
        self.goals.isNotifiedAboutEmergencyGoal.interp.addQualityConstraint(
            qc1)
        self.goals.isNotifiedAboutEmergencyGoal.interp.addQualityConstraint(
            qc2)

        # Provided Task QoS
        self.tasks.notifyCentralBySMSTask.setProvidedQuality(
            None, MpersMetrics.FALSE_NEGATIVE_PERCENTAGE, 10)

        self.tasks.notifyCentralByInternetTask.setProvidedQuality(
            None, MpersMetrics.FALSE_NEGATIVE_PERCENTAGE, 5)

        self.tasks.acceptEmergencyTask.setProvidedQuality(
            None, MpersMetrics.FALSE_NEGATIVE_PERCENTAGE, 30)

        self.tasks.confirmEmergencyByCallTask.setProvidedQuality(
            None, MpersMetrics.FALSE_NEGATIVE_PERCENTAGE, 5)

        self.tasks.processDataFromSensorsTask.setProvidedQuality(
            None, MpersMetrics.FALSE_NEGATIVE_PERCENTAGE, 15)

        self.tasks.collectDataFromSensorsTask.setProvidedQuality(
            None, MpersMetrics.SECONDS, 120)
        self.tasks.collectDataFromSensorsTask.setProvidedQuality(
            self.contexts.c3, MpersMetrics.SECONDS, 60)

        self.tasks.persistDataToDatabaseTask.setProvidedQuality(
            None, MpersMetrics.SECONDS, 5)

        self.tasks.identifySituationTask.setProvidedQuality(
            None, MpersMetrics.FALSE_NEGATIVE_PERCENTAGE, 20)

        self.tasks.notifyByMobileVibrationTask.setProvidedQuality(
            None, MpersMetrics.NOISE, 2)
        self.tasks.notifyBySoundAlertTask.setProvidedQuality(
            None, MpersMetrics.NOISE, 9)
        self.tasks.notifyByLightAlertTask.setProvidedQuality(
            None, MpersMetrics.NOISE, 0)
        self.tasks.centralCallTask.setProvidedQuality(
            None, MpersMetrics.NOISE, 7)

        self.tasks.sendInfoBySMSTask.setProvidedQuality(
            None, MpersMetrics.SECONDS, 65)
        self.tasks.sendInfoBySMSTask.setProvidedQuality(
            self.contexts.c8, MpersMetrics.SECONDS, 45)

        self.tasks.sendInfoByInternetTask.setProvidedQuality(
            None, MpersMetrics.SECONDS, 40)

        self.tasks.considerLastKnownLocationTask.setProvidedQuality(
            None, MpersMetrics.DISTANCE_ERROR, 900)
        self.tasks.considerLastKnownLocationTask.setProvidedQuality(
            None, MpersMetrics.SECONDS, 15)

        self.tasks.identifyLocationByVoiceCallTask.setProvidedQuality(
            None, MpersMetrics.DISTANCE_ERROR, 100)
        self.tasks.identifyLocationByVoiceCallTask.setProvidedQuality(
            self.contexts.c11, MpersMetrics.DISTANCE_ERROR, 300)
        self.tasks.identifyLocationByVoiceCallTask.setProvidedQuality(
            None, MpersMetrics.SECONDS, 45)

        self.tasks.accessLocationFromTriangulationTask.setProvidedQuality(
            None, MpersMetrics.DISTANCE_ERROR, 40)
        self.tasks.accessLocationFromTriangulationTask.setProvidedQuality(
            self.contexts.c11, MpersMetrics.DISTANCE_ERROR, 400)
        self.tasks.accessLocationFromTriangulationTask.setProvidedQuality(
            None, MpersMetrics.SECONDS, 30)

        self.tasks.accessLocationFromGPSTask.setProvidedQuality(
            None, MpersMetrics.DISTANCE_ERROR, 20)
        self.tasks.accessLocationFromGPSTask.setProvidedQuality(
            self.contexts.c11, MpersMetrics.DISTANCE_ERROR, 30)
        self.tasks.accessLocationFromGPSTask.setProvidedQuality(
            None, MpersMetrics.SECONDS, 45)

        self.tasks.accessDataFromDatabaseTask.setProvidedQuality(
            None, MpersMetrics.SECONDS, 20)

        self.tasks.getInfoFromResponsibleTask.setProvidedQuality(
            None, MpersMetrics.SECONDS, 25)
        self.tasks.getInfoFromResponsibleTask.setProvidedQuality(
            self.contexts.c11, MpersMetrics.SECONDS, 50)

        self.tasks.ambulanceDispatchDelegationTask.setProvidedQuality(
            None, MpersMetrics.SECONDS, 30)

        self.rootGoal = Goal(Decomposition.AND, "rootGoal")
        self.rootGoal = self.goals.respondToEmergencyGoal
