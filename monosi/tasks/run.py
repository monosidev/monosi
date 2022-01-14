from monosi.runner import Runner
from .base import ProjectTask, TaskBase

class RunnerTask(TaskBase):
    def __init__(self, args, config, monitors):
        super().__init__(args, config)
        self.monitors = monitors

    def run(self, *args, **kwargs):
        runner = Runner(self.config, self.monitors)
        runner.run()

class RunMonitorsTask(ProjectTask):
    def _create_tasks(self):
        if self.project is None:
            raise Exception("Project was not loaded before running monitors.")

        return [RunnerTask(self.args, self.config, self.project.monitors)]

    def _process_tasks(self):
        results = [task.run() for task in self.task_queue]
        return results
