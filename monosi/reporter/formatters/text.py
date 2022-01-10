from .base import baseFormatter

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