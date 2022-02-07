from core.common.events import track_event
from core.common.reporter import reporter

class BaseJob:
    @classmethod
    def run_job(cls, *args, **kwargs):
        job = cls()
        return job.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        raise NotImplementedError('Job not implemented.')

class MonitorJob(BaseJob):
    def __init__(self, task):
        self.task = task
        self.reporter = reporter
        self.task.reporter = self.reporter


    def run(self, *args, **kwargs):
        track_event(None, action="run_start", label="scheduled")
        self.reporter.start()
        self.task.run()
        self.reporter.finish()
        track_event(None, action="run_finish", label="scheduled")
