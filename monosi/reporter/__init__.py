from datetime import datetime
from time import time

from monosi.reporter.formatters.progress import ProgressFormatter

from .notifications import NotificationType

class Reporter:
    def __init__(self):
        self.tests = []
        self.skipped_tests = []
        self.failed_tests = []
        self.listeners = {}
        self.start_time = None
        self.stop_time = None
        self.monitor_finished_time = None

        formatter = ProgressFormatter()
        for notification_type in NotificationType.all():
            self.listeners[notification_type] = [formatter]
        
    def register_listener(self, listener, *notifications):
        for notification in notifications:
            self.listeners[notification].append(listener)

    def _listeners(self, notification):
        return list(self.listeners[notification])

    def monitor_started(self, monitor):
        self.start()
        self.notify(NotificationType.MONITOR_STARTED, monitor)

    def _reset(self):
        self.tests = []
        self.failed_tests = []
        self.load_time = None
        self.start_time = None
        self.stop_time = None
        self.monitor_finished_time = None

    def monitor_finished(self, monitor):
        self.monitor_finished_time = time()
        self.notify(NotificationType.MONITOR_FINISHED)
        self.finish()

    def test_started(self, test):
        self.tests.append(test)
        self.notify(NotificationType.TEST_STARTED)

    def test_finished(self, test):
        self.notify(NotificationType.TEST_FINISHED)

    def test_passed(self, test):
        self.notify(NotificationType.TEST_PASSED)

    def test_failed(self, test):
        self.failed_tests.append(test)
        self.notify(NotificationType.TEST_FAILED, test)

    def notify_non_test_exception(self, exception, context_description):
        pass

    def start(self):
        self._reset()
        self.start_time = time()

    def stop(self):
        self.stop_time = time()
        self.notify(NotificationType.STOP)

    def notify(self, notification_type: NotificationType, obj=None):
        # ensure listeners are ready
        try:
            [getattr(formatter, notification_type.value)(obj) for formatter in self._listeners(notification_type)]
        except Exception as e:
            print(e)


    def _load_time(self):
        if self.monitor_finished_time and self.start_time:
            return round(self.monitor_finished_time - self.start_time, 2)
        else:
            raise Exception("Could not calculate the load time.")

    def _total_time(self):
        if self.stop_time and self.start_time:
            return round(self.stop_time - self.start_time, 2)
        else:
            raise Exception("Could not calculate the total time.")

    def finish(self):
        self.stop()
        
        summary = {
            'failed_count': len(self.failed_tests),
            'skipped_count': 0,
            'test_count': len(self.tests),
            'total_time': self._total_time(),
            'load_time': self._load_time(),
        }

        self.notify(NotificationType.START_DUMP)
        self.notify(NotificationType.DUMP_SKIPPED)
        self.notify(NotificationType.DUMP_FAILURES, self.failed_tests)
        self.notify(NotificationType.DUMP_SUMMARY, summary)

