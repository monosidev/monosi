from monosi.events import track_event

from .run import RunMonitorsTask

class TestMonitorsTask(RunMonitorsTask):
    def _process_tasks(self):
        track_event(config, action='run_start', label='manual')
        super()._process_tasks()
        track_event(self.config, action="run_finish", label=str(len(self.monitors)))
