import logging
from math import sqrt
from typing import Any, List

from .base import Transformer


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
    def run(cls, metrics: List[Any], sensitivity: float):
        values = []
        zscores = []

        for metric in metrics:
            try:
                values.append(float(metric.value))
                mean = cls._mean(values)
                std_dev = cls._std_dev(values)
            except Exception as e:
                return []

            try:
                value = float(metric.value)
                if std_dev == 0:
                    z_score = 0
                else:
                    z_score = round(((value - mean) / std_dev), 2) 
                error = abs(z_score) > sensitivity 
                zscore_point = {
                    'metric_id': metric.id,
                    'expected_range_start': mean-(sensitivity*abs(std_dev)),
                    'expected_range_end': mean+(sensitivity*abs(std_dev)),
                    'error': error,
                    'zscore': z_score,
                }
                zscores.append(zscore_point)

            except Exception as e:
                logging.error(e)

        return zscores


class ZScoreTransformer(Transformer):
    @classmethod
    def _organize(cls, metrics):
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

    @classmethod
    def _transform(cls, metrics):
        sensitivity = 2.5
        zscores = []

        metrics = metrics[0][0] # TODO: Fix
        groups = cls._organize(metrics)

        for metric in groups:
            for column_name in groups[metric]:
                group_metrics = groups[metric][column_name]
                group_metrics.sort(key=lambda x: x.time_window_start)

                zscores += ZScoreAlgorithm.run(group_metrics, sensitivity)

        return zscores

    @classmethod
    def _original_schema(cls):
        # List of 
        return {
            "type": "object",
            "properties": {
                "metric": { "type": "string" },
                "column_name": { "type": "string" },
                "value": { "type": "string" },

                # A bunch of possible/optional metrics
            },
            "secret": [ ],
        }
        # raise NotImplementedError

    @classmethod
    def _normalized_schema(cls):
        return {
            "type": "object",
            "properties": {
                "zscore": { "type": "string" },
                "expected_range_start": { "type": "string" },
                "expected_range_end": { "type": "string" },
            },
            "secret": [ ],
        }
