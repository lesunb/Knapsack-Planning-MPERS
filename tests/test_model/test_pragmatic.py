from planning.common.model.context import Context
from planning.common.model.quality_constraint import QualityConstraint
from planning.common.model.common_metrics import CommonMetrics
from planning.common.model.pragmatic import Pragmatic
from planning.common.model.comparison import Comparison
from planning.common.model.decomposition import Decomposition


def test_shouldGetDifferentQualityConstraintsForDifferentContexts():
    aContext = Context("c1")
    anotherContext = Context("c2")

    aQC = QualityConstraint(aContext, CommonMetrics.METERS,
                            30, Comparison.LESS_OR_EQUAL_TO)
    anotherQC = QualityConstraint(
        anotherContext, CommonMetrics.METERS, 60, Comparison.LESS_OR_EQUAL_TO)

    goal = Pragmatic(Decomposition.AND, "G1")

    goal.interp.addQualityConstraint(aQC)
    goal.interp.addQualityConstraint(anotherQC)

    fullContext = []
    fullContext.append(aContext)

    assert aQC in goal.interp.getQualityConstraints(fullContext)

    anotherFullContext = []
    anotherFullContext.append(anotherContext)

    assert anotherQC in goal.interp.getQualityConstraints(anotherFullContext)
