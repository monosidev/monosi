from enum import Enum
from sys import stdout

class Color(Enum): # You may need to change color settings
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    ENDC = '\033[m'

class BaseFormatter:
    def __init__(self, output=stdout):
        self.output = output

    # def start(self, notification):
    #     self.start_sync_output()

    def write(self, text: str, color: Color):
        self.output.write(color.value)
        self.output.write(text)

    def stop(self, none_obj):
        pass

class TextFormatter(BaseFormatter):
    def message(self, notification):
        self.write('message', Color.ENDC)

    def dump_failures(self, failed_tests):
        for failed_test in failed_tests:
            self.write("Column: {column}\nMetric: {metric}\n\n".format(column=failed_test.column, metric=failed_test.metric), Color.RED)
        # if len(notification.failure_notifications) == 0: 
        #     return

        if len(failed_tests) == 0:
            self.write("\n\nAll tests passed.\n", Color.GREEN)

    def dump_summary(self, summary):
        # print(summary.fully_formatted)
        self.write('\nFinished in {total_time} seconds (SQL results took {load_time} seconds to load)\n'.format(
            total_time=summary['total_time'],
            load_time=summary['load_time'],
        ), Color.ENDC)

        color = Color.GREEN
        if summary['failed_count'] > 0:
            color = Color.RED

        self.write('{test_count} metrics, {failed_count} failures\n'.format(
            test_count=summary['test_count'],
            failed_count=summary['failed_count'],
        ), color)
        # self.write('dump_summary', Color.ENDC)

    def dump_pending(self, notification):
        # if len(notification.pending_examples) == 0: 
        #     return

        # print(notification.fully_formatted_pending_examples)
        # self.write('dump_pending', Color.YELLOW)
        pass

    def close(self):
        pass

class ProgressFormatter(TextFormatter):
    def monitor_started(self, monitor):
        self.write(monitor.info(), Color.ENDC)
        self.write('\n\n', Color.ENDC)

    def monitor_finished(self, monitor):
        # self.write('\n\nMonitor stopped\n', Color.ENDC)
        pass

    def dump_skipped(self, skipped_tests):
        pass

    def test_started(self, none_obj):
        self.write('', Color.ENDC)

    def test_finished(self, none_obj):
        self.write('', Color.ENDC)

    def test_passed(self, none_obj):
        self.write('.', Color.GREEN)
        
    def test_pending(self, none_obj):
        self.write('*', Color.YELLOW)

    def test_failed(self, none_obj):
        self.write('F', Color.RED)

    def start_dump(self, none_obj):
        # self.write('start_dump', Color.ENDC)
        pass

class FailureListFormatter(BaseFormatter):
    def example_failed(self, failure):
        self.write("{location}:{description}".format(
            location=failure.example.location, 
            description=failure.example.description
        ), Color.RED)

