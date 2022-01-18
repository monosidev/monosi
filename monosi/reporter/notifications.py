from enum import Enum

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
