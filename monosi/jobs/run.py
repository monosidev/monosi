from monosi.anomalies import ZScoreAnomalyDetector
from .base import JobBase, ProjectJob

class MonitorJob(JobBase):
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
    def run_job(cls, *args):
        job = cls(*args)
        results = job.run()

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

class MonitorsJob(ProjectJob):
    def _create_jobs(self):
        if self.project is None:
            raise Exception("Project was not loaded before running monitors.")

        return [MonitorJob(self.args, self.config, monitor) for monitor in self.project.monitors]

