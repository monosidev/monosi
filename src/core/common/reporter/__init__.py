from datetime import datetime
from time import time

from .formatters.progress import ProgressFormatter
from .notifications import NotificationType

class Reporter:
    def __init__(self):
        self.monitors = []
        self.tests = []
        self.passed_tests = []
        self.failed_tests = []
        self.start_time = None
        self.stop_time = None
        self.monitor_started_time = None
        self.monitor_stopped_time = None

        self.monitor = None
        self.listeners = {}

        formatter = ProgressFormatter()
        for notification_type in NotificationType.all():
            self.listeners[notification_type] = [formatter]
        
    def register_listener(self, listener, notifications=NotificationType.all()):
        for notification in notifications:
            self.listeners[notification].append(listener)

    def _listeners(self, notification):
        return list(self.listeners[notification])

    def monitor_started(self, monitor):
        self.start()
        self.monitor = monitor
        self.monitor_started_time = datetime.now()
        self.notify(NotificationType.MONITOR_STARTED, monitor)

    def _reset(self):
        self.tests = []
        self.failed_tests = []
        self.load_time = None
        self.monitor_started_time = None
        self.monitor_finished_time = None
        self.monitor = None

    def monitor_finished(self, monitor):
        self.monitor_finished_time = datetime.now()
        monitor_dict = {
            'monitor': monitor.to_dict(),
            'start_time': self.monitor_started_time,
            'stop_time': self.monitor_finished_time,
            'passed_metrics': [test.to_dict() for test in self.passed_tests],
            'failed_metrics': [test.to_dict() for test in self.failed_tests],
        }
        self.monitors.append(monitor_dict)
        self.monitor = None
        self.passed_tests = []
        self.failed_tests = []
        self.notify(NotificationType.MONITOR_FINISHED, monitor_dict)

    def test_started(self, test):
        self.tests.append(test)
        self.notify(NotificationType.TEST_STARTED)

    def test_finished(self, test):
        self.notify(NotificationType.TEST_FINISHED)

    def test_passed(self, test):
        self.passed_tests.append(test)
        self.notify(NotificationType.TEST_PASSED)

    def test_failed(self, test):
        self.failed_tests.append(test)
        self.notify(NotificationType.TEST_FAILED, test.to_dict())

    def notify_non_test_exception(self, exception, context_description):
        pass

    def start(self):
        self._reset()
        self.start_time = datetime.now()

    def stop(self):
        self.stop_time = datetime.now()
        self.notify(NotificationType.STOP)

    def notify(self, notification_type: NotificationType, obj=None):
        # ensure listeners are ready
        try:
            [getattr(formatter, notification_type.value)(obj) for formatter in self._listeners(notification_type)]
        except Exception as e:
            print(e)


    def _load_time(self):
        if self.monitor_finished_time and self.start_time:
            return self.monitor_finished_time - self.start_time
        else:
            raise Exception("Could not calculate the load time.")

    def _total_time(self):
        if self.stop_time and self.start_time:
            return self.stop_time - self.start_time
        else:
            raise Exception("Could not calculate the total time.")

    def finish(self):
        self.stop()
        
        summary = {
            'monitors': self.monitors,
            'total_time': self._total_time(),
            'load_time': self._load_time(),
        }
        self.monitors = []

        self.notify(NotificationType.START_DUMP)
        self.notify(NotificationType.DUMP_SKIPPED)
        self.notify(NotificationType.DUMP_FAILURES, self.failed_tests)
        self.notify(NotificationType.DUMP_SUMMARY, summary)

reporter = Reporter()
