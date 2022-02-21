from core.analyzer import ZScoreAnalyzer

from .extractors.sourcemetrics import MetricsExtractor
from .extractors.metrics import Extractor
from .loaders.metrics import Loader
from .loaders.zscores import ZScoreLoader
from .transformers.metrics import Transformer


class Pipeline:
    def __init__(self, extractor, transformer, loader):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def process(self, monitor):
        results = self.extractor.run(monitor)
        objs = self.transformer.run(results, monitor)
        self.loader.run(objs)
        return objs

class PipelineTask:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    @classmethod
    def _create_pipeline(cls, source, destinations):
        return Pipeline(
            extractor=Extractor(source, destinations),
            transformer=Transformer(),
            loader=Loader(destinations),
        )

    def _process_monitor(self, monitor):
        return self.pipeline.process(monitor)


class AnalyzerTask:
    def __init__(self, monitors, pipeline):
        self.monitors = monitors
        self.pipeline = pipeline

    @classmethod
    def _create_pipeline(cls, source, destinations):
        return Pipeline(
            extractor=MetricsExtractor(destinations[0]),
            transformer=ZScoreAnalyzer(),
            loader=ZScoreLoader(destinations),
        )

    @classmethod
    def from_source_and_destinations(cls, monitors, source, destinations):
        return cls(
            monitors=monitors,
            pipeline=cls._create_pipeline(source, destinations),
        )

    def _process_monitor(self, monitor):
        return self.pipeline.process(monitor)

    def run(self):
        return [self._process_monitor(monitor) for monitor in self.monitors]

class RunMonitorTask(PipelineTask):
    def __init__(self, monitor, pipeline):
        self.monitor = monitor
        self.pipeline = pipeline

    @classmethod
    def from_workspace(cls, monitor, workspace):
        source = workspace.integrations[monitor.source_name]
        destinations = [workspace.integrations[monitor.source_name]]

        return cls(
            monitor=monitor,
            pipeline=cls._create_pipeline(source, destinations),
        )

    def _process_monitor(self, monitor):
        return self.pipeline.process(monitor)

    def run(self):
        return self._process_monitor(self.monitor)


class RunMonitorsTask(PipelineTask):
    def __init__(self, monitors, pipeline):
        self.monitors = monitors
        self.pipeline = pipeline

    @classmethod
    def from_source_and_destinations(cls, monitors, source, destinations):
        return cls(
            monitors=monitors,
            pipeline=cls._create_pipeline(source, destinations),
        )

    def run(self):
        return [self._process_monitor(monitor) for monitor in self.monitors]

class RunAndAnalyzeTask:
    def __init__(self, run_task, analyze_task):
        self.run_task = run_task
        self.analyze_task = analyze_task

    @classmethod
    def from_source_and_destinations(cls, monitors, source, destinations):
        return cls(
            run_task=RunMonitorsTask.from_source_and_destinations(monitors, source, destinations),
            analyze_task=AnalyzerTask.from_source_and_destinations(monitors, source, destinations)
        )

    def run(self):
        self.run_task.run()
        self.analyze_task.run()


