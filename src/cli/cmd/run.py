from core.common.events import track_event
from core.monitor.models.base import Monitor

from .base import BaseCmd

class RunCmd(BaseCmd):
    def _create_tasks(self):
        return [definition.to_monitor(self.project.configuration) for definition in self.project.monitors]

    def _process_tasks(self):
        track_event(self.project, action="run_start", label="CLI")
        self.reporter.start()
        results = [task.run() for task in self.task_queue]
        self.reporter.finish()
        track_event(self.project, action="run_finish", label="CLI")

        return results
