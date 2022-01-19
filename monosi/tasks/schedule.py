from monosi.config.configuration import Configuration
from monosi.events import track_event
from monosi.tasks.base import ProjectTask
from monosi.tasks.run import RunnerTask

from monosi.scheduler.job import MonitorJob
from monosi.scheduler.manager import JobManager

class ScheduleMonitorsTask(ProjectTask):
    def __init__(self, args, config, manager: JobManager):
        super().__init__(args, config)
        self.manager = manager

    def _create_tasks(self):
        return []

    def _process_tasks(self):
        if self.project is not None:
            track_event(self.config, action="scheduling_monitors")

            for monitor in self.project.monitors:
                task = RunnerTask(self.args, self.config, [monitor])
                job = MonitorJob(task=task)
                self.manager.add_job(job, self.args, minutes=monitor.schedule.minutes)

    @classmethod
    def from_args(cls, args, manager: JobManager):
        try:
            config = Configuration.from_args(args)
        except:
            raise Exception("There was an issue creating the task from args.")

        return cls(args, config, manager)

