from monosi.events import track_event

from .base import MonitorsTask

class TestMonitorsTask(MonitorsTask):
    def __init__(self, args, config):
        track_event(config, action='run_start', label='manual')
        super().__init__(args, config)

    def _process_tasks(self):
        results = [task.run() for task in self.task_queue]
        return results
