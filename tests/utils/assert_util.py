def assertPlan(plan, tasks):
    
    if tasks is None:
        if plan is None:
            return True
        else:
            return False

    if plan is None:
        return False

    planTasks = plan.getTasks()

    print("======== Tasks ========")

    for a in tasks:
        print(a.identifier)

    print("======== Plan Tasks ========")

    for b in planTasks:
        print(b.identifier)

    success = True

    for task in tasks:
        if task not in planTasks:
            success = False
            #print(f"Task {task.identifier} should be in Plan")                
            
    for pTask in planTasks:
        if pTask not in tasks:
            success = False
            #print(f"Task {pTask.identifier} should not be in Plan")

    return success


def assertPlan2(plan, plan2):
    
    if plan2 is None:
        if plan is None:
            return True
        else:
            return False

    if plan is None:
        return False

    diff = False
    
    planTasks = plan.getTasks()
    plan2Tasks = plan2.getTasks()

    setPlan1 = set(planTasks)
    setPlan2 = set(plan2Tasks)

    print("Plan 1 tasks: ", planTasks)
    print("Plan 2 tasks: ", plan2Tasks)
    print("Diference between plans: ", setPlan1-setPlan2)

    for pTask in planTasks:
        for ptask2 in plan2Tasks:
            print(f"Task plan 1 {pTask.identifier} - {pTask.providedQualityLevels} || Task Plan 2 {ptask2.identifier} - {ptask2.providedQualityLevels}")
            if pTask not in plan2Tasks:
                diff = True
                #print(f"Task plan 1 {pTask.identifier} - {pTask.providedQualityLevels} || Task Plan 2 {ptask2.identifier} - {ptask2.providedQualityLevels}")
                print(f"Task {pTask.identifier} diferent in Plans")
                print(f"Task {pTask.providedQualityLevels} Quality level")

    return diff        