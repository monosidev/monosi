from enum import Enum

from monosi.anomalies import AnomalyDetectorTest

class NotificationType(Enum):
    MONITOR_STARTED = 'monitor_started'
    MONITOR_FINISHED = 'monitor_finished'
    TEST_STARTED = 'test_started'
    TEST_FINISHED = 'test_finished'
    TEST_PASSED = 'test_passed'
    TEST_FAILED = 'test_failed'
    START_DUMP = 'start_dump'
    DUMP_SKIPPED = 'dump_skipped'
    DUMP_FAILURES = 'dump_failures'
    DUMP_SUMMARY = 'dump_summary'
    STOP = 'stop'

    @classmethod
    def all(cls):
        return cls.__members__.values()

class StartNotification:
    count: int

class TestNotification:
    test: AnomalyDetectorTest

class MonitorNotification:
    def __init__(self, reporter):
        self.reporter = reporter

    def tests(self):
        return self.reporter.tests

    def failed_tests(self):
        return self.reporter.failed_tests

    def skipped_tests(self):
        return self.reporter.skipped_tests

class FailedTestNotification:
    pass

class SkippedTestNotification:
    pass

class MonitorNotification:
    pass

class MessageNotification:
    pass

class SummaryNotification:
    pass
