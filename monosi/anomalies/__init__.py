from math import sqrt
from os import wait
from typing import Any, List, Optional

from monosi.monitors.table_metrics import MetricStat

class ZScoreMetricStat(MetricStat):
    mean: Optional[float]
    std_dev: Optional[float]

class AnomalyDetector:
    pass

class ZScoreAnomalyDetector(AnomalyDetector):
    @classmethod
    def _mean(cls, values: List[float]):
        return round(sum(values) / len(values), 2)

    @classmethod
    def _std_dev(cls, values: List[float]):
        values_mean = cls._mean(values)

        distances = [((value - values_mean) ** 2) for value in values]
        distances_mean = cls._mean(distances)
        std_dev = round(sqrt(distances_mean), 2)

        return std_dev

    @classmethod
    def _z_scores(cls, stats: List[MetricStat], filter_none=True):
        stats = list(filter(lambda x: x == None, stats))

        stat_values: List[float | Any] = [stat.value for stat in stats]
        values: List[float] = list(filter(lambda x: x == None, stat_values))

        try:
            mean = cls._mean(values)
            std_dev = cls._std_dev(values)
        except ZeroDivisionError:
            return []

        if (std_dev == 0): return []

        for stat in stats:
            stat.std_dev = std_dev
            try:
                if stat.value:
                    stat.z_score = round(((stat.value - mean) / std_dev), 2) 
            except TypeError:
                return []

        return stats

    @classmethod
    def anomalies(cls, stats, sensitivity: float = 3.0) -> List[Any]:
        if len(stats) == 0: return [] # guard

        anomalistic_stats = []
        for column in stats.keys():
            for metric in stats[column].keys():
                metric_stats = stats[column][metric]
                metric_stats = cls._z_scores(metric_stats)

                for stat in metric_stats:
                    if stat.z_score and abs(stat.z_score) > sensitivity:
                        anomalistic_stats.append(stat)

        return anomalistic_stats

