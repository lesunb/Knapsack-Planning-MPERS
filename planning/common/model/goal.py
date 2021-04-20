from planning.common.model.refinement import Refinement
from planning.common.model.plan import Plan
from planning.common.model.decomposition import Decomposition


class Goal(Refinement):
    def __init__(self, decomposition, identifier):
        Refinement.__init__(self, identifier)
        self.decomposition = decomposition

    def myType(self):
        return Refinement().GOAL