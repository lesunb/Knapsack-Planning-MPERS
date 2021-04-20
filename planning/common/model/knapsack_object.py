from planning.common.model.task import Task


class KnapsackObject(Task):
  def __init__(self, task):
    Task.__init__(self, task)

  def getValue(self, context):
    weight = self.getWeight(context)
    if weight > 0:
        value = 1/weight
    elif weight == 0:
        value =  1
    else:
        value =  0

    return value

  def getWeight(self, context):
    qc = 0

    # get the qualities constraints from curent active context
    for metric in self.providedQualityLevels.keys():
        myQC = self.myProvidedQuality(metric, context)

        if myQC is not None:
            qc = qc + myQC

    return qc

  # Return quality value if exists
  def myProvidedQuality(self, metric, contextSet):
    myQuality = 0
    initQuality = False
    # Check if the metric was already in Provided Qualities
    if metric not in self.providedQualityLevels.keys():
        message = "Metric: {0} not found".format(metric.name)
        print(message)
        return None
    # get metric
    metricQL = self.providedQualityLevels[metric]

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

  # Set task provided quality from baseline or context
  def setProvidedQuality(self, context, metric, value):
      metricMap = {}
      # Check if the metric was already in Provided Qualities
      if metric in self.providedQualityLevels:
          metricMap = self.providedQualityLevels[metric]
          # if yes, replace with new value
          metricMap[context] = value
          self.providedQualityLevels[metric] = metricMap
      else:
          metricMap[context] = value
          # if no, add
          self.providedQualityLevels[metric] = metricMap

