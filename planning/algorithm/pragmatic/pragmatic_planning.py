from planning.common.model.refinement import Refinement
from planning.common.model.plan import Plan
from planning.common.model.decomposition import Decomposition
from planning.common.exceptions.metric_not_found import MetricNotFoundException


class PragmaticPlanning:
    
    # check if refinement(goals or taks) is applicable in current active context
    def isApplicable(self, dep, current):
        returnValue = False

        # check if is there is no context
        if dep.applicableContext is None:
            returnValue = True

        if len(dep.nonapplicableContexts) > 0:
            returnValue = True
        # iterates over contexts to return if is applicable or not
        for context in current:
            if context in dep.nonapplicableContexts:
                return False
            if dep.applicableContext:
                if context in dep.applicableContext:
                    returnValue = True

        return returnValue

    # If is a pragmatic goal merge the interpretations
    def isAchievablePlan(self, goal, current, interp):
        if type(goal).__name__ == 'Pragmatic':
            return goal.isAchievable(current, interp)
        else:
            return self.isAchievable(goal, current, interp)

    # Recursive function to choose plan
    def isAchievable(self, goal, current, interp):
        # Check if Goal is achievable for current context
        if not self.isApplicable(goal, current):
            return None
        # Active taks or goals that are dendencies for self.goal achievement
        dependencies = goal.getApplicableDependencies(current)

        if goal.decomposition == Decomposition.OR:
            # if decomposition is OR return first achievable plan from dependencies list
            for dep in dependencies:
                if(dep.myType() is Refinement().GOAL):
                    if type(dep).__name__ == 'Pragmatic':
                        dep.isAchievable(current, interp)
                    else:
                        plan = self.isAchievable(dep, current, interp)
                elif(dep.myType() is Refinement().TASK):
                    plan = self.isAchievableTask(dep, current, interp)
                else:
                    return None
                if plan:
                    return plan
            return None
        else:
            # else decomposition is AND return achievables plans list from dependencies list
            complete = Plan()
            for dep in dependencies:
                if(dep.myType() is Refinement().GOAL):
                    if type(dep).__name__ == 'Pragmatic':
                        plan = dep.isAchievable(current, interp)
                    else:
                        plan = self.isAchievable(dep, current, interp)
                elif(dep.myType() is Refinement().TASK):
                    plan = self.isAchievableTask(dep, current, interp)
                else:
                    return None

                if plan:
                    complete.add(plan)
                else:
                    return None
            if len(complete.getTasks()) > 0:
                return complete
            else:
                return None

    def abidesByInterpretation(self, task, interp, current):
        # Return if the quality from the task is suitable
        feasible = True
        if interp is None:
            return True

        currentQcs = interp.getQualityConstraints(current)
        # get the qualities constraints from curent active context
        for qc in currentQcs:
            try:
                myQC = self.myProvidedQuality(task, qc.metric, current)
                if myQC is not None:
                    # check if metric fits the interpretation constrain
                    if not qc.abidesByQC(myQC, qc.metric):
                        feasible = False
            except MetricNotFoundException:
                pass
        # get the qualities constraints from baseline
        if interp.getQualityConstraints([None]):
            for qc in interp.getQualityConstraints([None]):
                try:
                    myQC = self.myProvidedQuality(task, qc.metric, current)
                    if myQC is not None:
                        if not qc.abidesByQC(myQC, qc.metric):
                            feasible = False
                except MetricNotFoundException:
                    pass

        return feasible


    # Return quality value if exists
    def myProvidedQuality(self, task, metric, contextSet):
        myQuality = 0
        initQuality = False
        # Check if the metric was already in Provided Qualities
        if metric not in task.providedQualityLevels.keys():
            message = "Metric: {0} not found".format(metric.name)
            print(message)
            return None
        # get metric
        metricQL = task.providedQualityLevels[metric]

        # getting baseline
        if None in metricQL:
            myQuality = metricQL[None]
            initQuality = True
        # test the qualities of active contexts
        for current in contextSet:
            if metricQL.get(current) is None:
                continue
            if not initQuality:
                myQuality = metricQL.get(current)
                initQuality = True
            else:
                # check if less is better for that metric
                if metric.getLessIsBetter():
                    if(myQuality > metricQL[current]):
                        myQuality = metricQL[current]
                elif(myQuality < metricQL[current]):
                    myQuality = metricQL[current]

        return myQuality

    def isAchievableTask(self, task, current, interp):
        # check if the task is applicable for that context
        if not self.isApplicable(task, current):
            return None
        # test if quality fit and if return it with Plan to be added
        if self.abidesByInterpretation(task, interp, current):
            return Plan(task)
        else:
            return None
