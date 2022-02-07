from .base import Color
from .text import TextFormatter

class ProgressFormatter(TextFormatter):
    def monitor_started(self, monitor):
        # self.write(monitor.info(), Color.ENDC)
        self.write('\n\n', Color.ENDC)

    def _monitor_header(self, monitor):
        header = ""
        if monitor['type'] == 'table':
            header += "\nTable Health: {}".format(monitor.get('name') or monitor.get('table'))
        elif monitor['type'] == 'custom':
            header += "\nCustom Monitor: {}".format(monitor.get('name') or monitor.get('sql'))
        elif monitor['type'] == 'schema':
            header += "\nSchema Monitor: {}".format(monitor.get('name') or monitor.get('table'))

        if monitor.get('description'):
            header += "\nDescription: {}".format(monitor.get('description'))

        return header


    def monitor_finished(self, monitor):
        monitor_dict = monitor['monitor']

        self.write(self._monitor_header(monitor_dict), Color.ENDC)

        if len(monitor['failed_metrics']) > 0:
            for metric in monitor['failed_metrics']:
                self.write("\n", Color.RED)
                self.write(metric['message'], Color.RED)
        else:
            self.write("\nNo Failures.", Color.ENDC)

        self.write("\n\nStart: {}\tStop: {}\n\n".format(monitor['start_time'], monitor['stop_time']), Color.ENDC)

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
