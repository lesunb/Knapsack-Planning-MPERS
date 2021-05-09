from planning.common.model.metric import Metric
from planning.common.model.metric_restrictions import MetricRestrictions

class MpersMetrics:
    FALSE_NEGATIVE_PERCENTAGE = Metric("False Negative")
    NOISE = Metric('Noise')
    SECONDS = Metric('Seconds')
    ERROR = Metric('Error')
    DISTANCE_ERROR = MetricRestrictions('Distance')
    METERS = Metric('Meters')