from planning.common.model.goal import Goal
from planning.common.model.interpretation import Interpretation
from planning.algorithm.knapsack.knapsack_planning import KnapsackPlanning

class Knapsack(Goal):

    def __init__(self, decomposition, identifier):
        Goal.__init__(self, decomposition, identifier)

        self.interp = Interpretation()
        self.maxValue = 0
        self.task = []
        self.value = []
        self.weight = []
        self.group = []
        self.solution = []

    def mergeKnapsack(self, newKnapsack, interp):
        self.task.extend(newKnapsack.task)
        self.value.extend(newKnapsack.value)
        self.weight.extend(newKnapsack.weight)
        self.group.extend(newKnapsack.group)

        newInterp = Interpretation()
        newInterp.merge(self.interp)
        newInterp.merge(interp)

    def setItem(self, task, value, weight, group):
        self.task.append(task)
        self.value.append(value)
        self.weight.append(weight)
        self.group.append(group)

    def isAchievable(self, current, interp):
        newInterp = Interpretation()
        newInterp.merge(self.interp)
        newInterp.merge(interp)

        return KnapsackPlanning().isAchievable(self, current, newInterp)
