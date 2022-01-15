from .base import BaseFormatter, Color

class TextFormatter(BaseFormatter):
    def message(self, notification):
        self.write('message', Color.ENDC)

    def dump_failures(self, failed_tests):
        # TODO: Consider Failures Formatter
        if len(failed_tests) == 0:
            self.write('', Color.ENDC)
            # self.write("\n\nAll tests passed.\n", Color.GREEN)
        else:
            self.write("\nFailures\n", Color.RED)

        for failed_test in failed_tests:
            self.write("\tColumn: {}\n".format(failed_test.column), Color.RED)
            self.write("\tMetric: {}\n".format(failed_test.metric), Color.RED)
            self.write("\tAnomalies: {}\n".format(len(failed_test.anomalies)), Color.RED)
            self.write("\n", Color.RED)
            # for anomaly in failed_test.anomalies:
            #     self.write("\tValue: {value}\n\tExpected Range: {start} - {stop}\n\tTime Window: {time_start} - {time_end}\n\n".format(
            #         value=anomaly.point.value,
            #         start=anomaly.expected_range_start,
            #         stop=anomaly.expected_range_end,
            #         time_start=anomaly.point.window_start,
            #         time_end=anomaly.point.window_end,
            #     ), Color.RED)

        # if len(notification.failure_notifications) == 0: 
        #     return


    def dump_summary(self, summary):
        # print(summary.fully_formatted)
        self.write('\n\nFinished in {total_time} seconds (SQL results took {load_time} seconds to load)\n'.format(
            total_time=summary['total_time'],
            load_time=summary['load_time'],
        ), Color.ENDC)

        color = Color.GREEN
        if summary['failed_count'] > 0:
            color = Color.RED

        self.write('{test_count} metrics, {failed_count} failures\n\n\n'.format(
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
