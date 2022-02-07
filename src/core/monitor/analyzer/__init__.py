import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from core.common.drivers.column import Table

from core.monitor.models.custom import CustomMetric
from core.monitor.models.schema import SchemaMetric
from core.monitor.models.table import ColumnMetric

from .data import Data
from .schema import SchemaComparisonTest
from .threshold import ThresholdTest
from .zscore import ZScoreTest

class Analyzer:
    def __init__(self, reporter):
        self.reporter = reporter

    def _create_test(self, metric, data: Data):
        if isinstance(metric, ColumnMetric):
            return ZScoreTest.from_metric(metric, data)
        elif isinstance(metric, CustomMetric):
            return ThresholdTest.from_metric(metric, data)
        elif isinstance(metric, SchemaMetric):
            return SchemaComparisonTest.from_metric(metric, data)
        else:
            logging.warning("Data returned from the database did not contain data for a metric defined in the monitor.")
            raise Exception("Could not create test because the monitor was not recognized.")

    def test(self, metric, data):
        test = self._create_test(metric, data)
        result = None
        
        try:
            self.reporter.test_started(self)
            result = test.run()
            if result.status == True:
                self.reporter.test_passed(result)
            else:
                self.reporter.test_failed(result)
        finally:
            self.reporter.test_finished(result)
        
        return result

    def analyze(self, monitor, results):
        data = Data.from_results(results)
        results = {}

        for metric in monitor.retrieve_metrics():
            result = self.test(metric, data)
            results[metric.alias()] = result

        return results
