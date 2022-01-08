from .base import MonitorsTask

class TestMonitorsTask(MonitorsTask):
    def _process_tasks(self):
        results = [task.run() for task in self.task_queue]
        return results
