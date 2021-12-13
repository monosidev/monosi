import abc
from typing import List, Optional

from monosi.config.configuration import Configuration
from monosi.project import Project

class JobBase:
    def __init__(self, args, config):
        self.args = args
        self.config = config

    @classmethod
    def from_args(cls, args):
        try:
            config = Configuration.from_args(args)
        except:
            raise Exception("There was an issue creating the job from args.")

        return cls(args, config)

    @classmethod
    def run_job(cls, *args, **kwargs):
        job = cls(*args)
        return job.run(*args, **kwargs)

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError('Implementation for job does not exist.')

class ProjectJob(JobBase):
    def __init__(self, args, config):
        super().__init__(args, config)
        self.project: Optional[Project] = None
        self.job_queue: List[JobBase] = []

    def load_project(self):
        self.project = Project.from_configuration(self.config)
        self.job_queue = self._create_jobs()

    @abc.abstractmethod
    def _create_jobs(self):
        raise NotImplementedError

    def _process_jobs(self):
        results = [job.run() for job in self.job_queue]
        return results

    def run(self):
        self._initialize()
        return self._process_jobs()

    def _initialize(self):
        self.load_project()

