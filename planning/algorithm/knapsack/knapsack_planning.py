from planning.common.model.refinement import Refinement
from planning.common.model.plan import Plan
from planning.common.model.decomposition import Decomposition
from planning.common.exceptions.metric_not_found import MetricNotFoundException
from planning.common.model.interpretation import Interpretation


class KnapsackPlanning:
    
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
        newInterp = self.mergeInterp(goal, interp)
        return self.isAchievable(goal, current, newInterp)

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
                    newInterp = self.mergeInterp(goal, interp)
                    self.isAchievable(dep, current, newInterp)
                elif(dep.myType() is Refinement().TASK):
                    if self.isAchievableTask(dep, current, interp):
                        value = dep.getValue(current)
                        weight = dep.getWeight(current)
                        goal.setItem(dep, value, weight, goal.identifier)

            if goal.parentNode.decomposition is Decomposition.AND:
                if goal.task:
                    if goal.parentNode.parentNode is None:
                        plan = self.createKnapsackTable(interp, goal)

                        if plan:
                            return plan

                    else:
                        return goal
                else:
                    maxTask = None
                    maxValue = 0
                    for dep in goal.dependencies:
                        if dep.maxValue > maxValue:
                            maxValue = dep.maxValue
                            maxTask = dep

                return maxTask.solution

            return None
        else:
            # else decomposition is AND return achievables plans list from dependencies list
            for dep in dependencies:
                plan = None
                complete = None
                if(dep.myType() is Refinement().GOAL):
                    newInterp = self.mergeInterp(goal, interp)
                    plan = self.isAchievable(dep, current, newInterp)
                elif(dep.myType() is Refinement().TASK):
                    if self.isAchievableTask(dep, current, interp):
                        value = dep.getValue(current)
                        weight = dep.getWeight(current)
                        goal.setItem(dep, value, weight, goal.identifier)
                else:
                    return None
                
                if plan:
                    goal.mergeKnapsack(plan, plan.interp)
                    
            if goal.task:
                if goal.parentNode.decomposition is Decomposition.OR:
                    complete = self.createKnapsackTable(interp, goal)
                if goal.parentNode.decomposition is Decomposition.AND:
                    complete = goal
                    
            return complete

    def mergeInterp(self, goal, interp):
        newInterp = Interpretation()
        newInterp.merge(goal.interp)
        newInterp.merge(interp)

        return newInterp    

    
    def createKnapsackTable(self, interp, goal):
        task = goal.task
        value = goal.value
        weight = goal.weight
        groupName = goal.group
        group = []
        N = len(value)
        g = 0

        for i in range(N):
            if i == 0:
                group.append(g)
            elif groupName[i] == groupName[i-1]:
                group.append(g)
            else:
                g = g+1
                group.append(g)

        for index in interp.contextDependentInterpretation:
            capacity = interp.contextDependentInterpretation[index][0].value

            if g > 0:
                capacity = capacity * g+1

        K = [[0 for x in range(N)] for x in range(capacity)]
        solution = [[None for x in range(N)] for x in range(capacity)]

        for n in range(0, N):
            for w in range(1, capacity+1):
                option1 = self.getMax(group[n]-1, K[n], group, n)
                option2 = 0
                option3 = self.getMax(group[n], K[n], group, n)

                if weight[n] <= w:
                    option2 = value[n] + self.getMax(group[n] - 1, K[(w-1) - weight[n]], group, n)

                K[w-1][n] = max(option1, option2)

                if (option2 > option1) and (option2 > option3):
                    solution[w-1][n] = task[n]

        take, maxValue = self.getSolution(N, capacity, solution, group, K, weight)

        goal.maxValue = maxValue
        goal.solution = take

        return take

    def getMax(self, group, row, groups, n):
        max = 0

        for i in range(n):
            if groups[i] == group:
                if row[i] > max:
                    max = row[i]
        
        return max

    def getSolution(self, N, W, sol, group, matrix, weight):
        solution = Plan()
        lastTakenGroup = -1
        
        for n in range(0, N):
            for w in range(1, W):        
                if sol[w][n] is not None and self.calculateIsMax(n, w, group, matrix, N):
                    if group[n] == lastTakenGroup:
                        continue
                    solution.addTask(sol[w][n])
                    maxValue = matrix[w][n]
                    w = w - weight[n]
                    lastTakenGroup = group[n]
        
        return solution, maxValue

    def calculateIsMax(self, n, w, groups, matrix,  N):
        group = groups[n]
        max = 0
        for i in range(N):
            if(groups[i] == group):
                if(matrix[w][i] > max):
                    max = matrix[w][i]
            
        
        return matrix[w][n] == max

    def abidesByInterpretation(self, task, interp, current):
        # Return if the quality from the task is suitable
        feasible = True
        myQC = 0

        if interp is None:
            return True

        currentQcs = interp.getQualityConstraints(current)
        # get the qualities constraints from curent active context
        for qc in currentQcs:
            try:
                myQC = task.myProvidedQuality(qc.metric, current)
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
                    myQC = task.myProvidedQuality(qc.metric, current)
                    if myQC is not None:
                        if not qc.abidesByQC(myQC, qc.metric):
                            feasible = False
                except MetricNotFoundException:
                    pass

        return feasible


    def isAchievableTask(self, task, current, interp):
        # check if the task is applicable for that context
        if not self.isApplicable(task, current):
            return None
        # test if quality fit and if return it with Plan to be added
        if self.abidesByInterpretation(task, interp, current):
            return True
        else:
            return None

