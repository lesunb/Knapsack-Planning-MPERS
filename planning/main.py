from planning.algorithm.pragmatic.pragmatic_planning import PragmaticPlanning
from tests.test_data.mpers_model import MpersModel
from planning.algorithm.knapsack.knapsack_planning import KnapsackPlanning
from tests.test_data.mpers_knapsack_model import MpersKnapsackModel


def main():
    print("Planejamento MPERS")
    mpers = MpersKnapsackModel()
    fullcontext = [mpers.contexts.c1, 
    mpers.contexts.c2, mpers.contexts.c3, 
    mpers.contexts.c4, mpers.contexts.c8]
    plan = PragmaticPlanning().isAchievablePlan(mpers.rootGoal, fullcontext, None)

    print(plan)

if __name__ == "__main__":
    main()