from planning.common.model.goal import Goal
from planning.common.model.interpretation import Interpretation
from planning.algorithm.pragmatic.pragmatic_planning import PragmaticPlanning

class Pragmatic(Goal):

    def __init__(self, decomposition, identifier):
        Goal.__init__(self, decomposition, identifier)

        self.interp = Interpretation()

    def isAchievable(self, current, interp):
        newInterp = Interpretation()
        newInterp.merge(self.interp)
        newInterp.merge(interp)

        return PragmaticPlanning().isAchievable(self, current, newInterp)
