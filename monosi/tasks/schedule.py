from monosi.events import track_event
from monosi.tasks.base import TaskBase
from monosi.tasks.run import RunnerTask

from monosi.scheduler.job import MonitorJob
from monosi.scheduler.manager import JobManager

class ScheduleMonitorsTask(TaskBase):
    def __init__(self, args, config, manager, monitors):
        super.__init__(args, config)
        self.manager = manager
        self.monitors = monitors

    def run(self, *args, **kwargs):
        track_event(self.config, action="scheduling_monitors")
        for monitor in self.monitors:
            job = RunnerTask(self.args, self.config, [monitor])
            self.manager.add_job(job, self.args, minutes=monitor.schedule.minutes)

