import logging
from math import sqrt
from dataclasses import dataclass
from typing import List

from core.models.metadata.metric import MsiMetric
from core.models.zscore import ZScore


class ZScoreAlgorithm:
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
    def run(cls, metrics: List[MsiMetric], sensitivity: float):
        values = []
        zscores = []
        for metric in metrics:
            values.append(float(metric.value))
            try:
                mean = cls._mean(values)
                std_dev = cls._std_dev(values)
            except ZeroDivisionError:
                return []

            try:
                value = float(metric.value)
                if std_dev == 0:
                    z_score = 0
                else:
                    z_score = round(((value - mean) / std_dev), 2) 
                error = abs(z_score) > sensitivity 
                zscore_point = ZScore(
                    metric_id=metric.id,
                    expected_range_start=mean-(sensitivity*abs(std_dev)),
                    expected_range_end=mean+(sensitivity*abs(std_dev)),
                    error=error,
                    zscore=z_score,
                )
                zscores.append(zscore_point)

            except Exception as e:
                logging.error(e)

        return zscores

class ZScoreAnalyzer:
    def __init__(self, sensitivity=2.5):
        self.sensitivity = sensitivity

    def _organize(self, metrics):
        groups = {}
        for obj in metrics:
            metric = obj.metric
            column_name = obj.column_name

            if metric not in groups:
                groups[metric] = {}

            if column_name not in groups[metric]:
                groups[metric][column_name] = []

            groups[metric][column_name].append(obj)

        return groups

    def run(self, metrics, monitor): # TODO: Optimize
        zscores = []
        groups = self._organize(metrics)

        for metric in groups:
            for column_name in groups[metric]:
                group_metrics = groups[metric][column_name]
                group_metrics.sort(key=lambda x: x.time_window_start)

                zscores += ZScoreAlgorithm.run(group_metrics, self.sensitivity)

        return zscores

        

    # @classmethod
    # def run(cls, monitor_id, dest_config):
    #     pass

