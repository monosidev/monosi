from .base import Color
from .text import TextFormatter

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
