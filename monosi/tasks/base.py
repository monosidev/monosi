import abc
from typing import List, Optional

from monosi.anomalies import ZScoreAnomalyDetector
from monosi.config.configuration import Configuration
from monosi.project import Project

class TaskBase:
    def __init__(self, args, config):
        self.args = args
        self.config = config

    @classmethod
    def from_args(cls, args):
        try:
            config = Configuration.from_args(args)
        except:
            raise Exception("There was an issue creating the task from args.")

        return cls(args, config)

    @classmethod
    def run_task(cls, *args, **kwargs):
        task = cls(*args)
        return task.run(*args, **kwargs)

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError('Implementation for task does not exist.')

class ProjectTask(TaskBase):
    def __init__(self, args, config):
        super().__init__(args, config)
        self.project: Optional[Project] = None
        self.task_queue: List[TaskBase] = []

    def load_project(self):
        self.project = Project.from_configuration(self.config)
        self.task_queue = self._create_tasks()

    def _initialize(self):
        self.load_project()

    @abc.abstractmethod
    def _create_tasks(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _process_tasks(self):
        raise NotImplementedError

    def run(self):
        self._initialize()
        return self._process_tasks()

class MonitorTask(TaskBase):
    def __init__(self, args, config, monitor):
        super().__init__(args, config)
        self.monitor = monitor

    def compile_and_execute(self):
        driver_config = self.config.config

        return self.monitor.execute(driver_config)

    def detect_anomalies(self, stats):
        anomalies = ZScoreAnomalyDetector.anomalies(stats)

        return anomalies

    @classmethod
    def run_task(cls, *args):
        task = cls(*args)
        results = task.run()

    def run(self):
        stats = self.compile_and_execute()
        anomalies = self.detect_anomalies(stats)
        for anomaly in anomalies:
            print("There was an anomaly with table {table}'s column {column} and a value of {value} for the metric {metric}".format(
                table=anomaly.table,
                column=anomaly.column,
                value=str(anomaly.value),
                metric=anomaly.metric,
            ))

class MonitorsTask(ProjectTask):
    def _create_tasks(self):
        if self.project is None:
            raise Exception("Project was not loaded before running monitors.")

        return [MonitorTask(self.args, self.config, monitor) for monitor in self.project.monitors]
