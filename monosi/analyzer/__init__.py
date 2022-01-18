import logging

from monosi.monitors.custom import CustomMetric
from monosi.monitors.table import ColumnMetric

from .data import Data, DataPoint, TableData
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
        else:
            logging.warning("Data returned from the database did not contain data for a metric defined in the monitor.")
            raise Exception("Could not create test because the monitor was not recognized.")

    def test(self, metric, data):
        test = self._create_test(metric, data)
        
        try:
            self.reporter.test_started(self)
            result = test.run()
            if not len(result.anomalies()) > 0:
                self.reporter.test_passed(test)
            else:
                self.reporter.test_failed(test)
        finally:
            self.reporter.test_finished(metric)
        
        return result

    def analyze(self, monitor, results):
        data = Data.from_results(results)
        results = {}

        for metric in monitor.retrieve_metrics():
            result = self.test(metric, data)
            results[metric.alias()] = result

        return results

