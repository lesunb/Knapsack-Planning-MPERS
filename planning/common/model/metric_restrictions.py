from planning.common.model.metric_type import MetricType


class MetricRestrictions():
    def __init__(self, name, lessIsBetter=False):
        self.name = name
        self.lessIsBetter = lessIsBetter

    def getLessIsBetter(self):
        return self.lessIsBetter

    def getType(self):
        return MetricType.RESTRICTION
