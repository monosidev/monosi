from dataclasses import dataclass
import itertools
from typing import Any, Dict, List
from ingestion.sources import SourceFactory

from ingestion.sources.base import Source
from ingestion.task import Task

from .pipeline import Pipeline


def flatten(arr):
    return list(itertools.chain.from_iterable(arr))

@dataclass
class CollectorState:
    discovered_data: Any = None
    fetched_data: Any = None

@dataclass
class Collector:
    source: Source
    filters: List[Any] # pure py function
    pipelines: List[Pipeline]
    state: CollectorState = CollectorState()

    def _create_tasks(self):
        extractor = self.source.extractor()
        task_units = self.source.task_units(self.state.discovered_data)

        return [Task(extractor=extractor, units=[unit]) for unit in task_units]

    def _filter_data(self, discovered_data):
        for data_filter in self.filters:
            discovered_data = data_filter(discovered_data)
        return discovered_data

    @classmethod
    def from_configuration(cls, source_dict: Dict[str, Any], filters = [], pipelines = []):
        source = SourceFactory.create(source_dict)

        return cls(source=source, filters=filters, pipelines=pipelines)

    def discover_data(self):
        discovery_query = self.source.discovery_query()
        extractor = self.source.extractor()

        discovered_data = extractor.run(discovery_query)
        discovered_data_filtered = self._filter_data(discovered_data)

        self.state.discovered_data = discovered_data_filtered

    def fetch_data(self):
        # Run tasks
        for task in self._create_tasks():
            task_results_gen = task.run()
            while True:
                try:
                    units_results_gen = next(task_results_gen)
                    
                    while True:
                        try:
                            self.state.fetched_data = next(units_results_gen)
                            self.pass_data()
                        except StopIteration:
                            break
                except StopIteration:
                    break

    def pass_data(self):
        if self.state.fetched_data is None:
            return

        print(self.state.fetched_data)
        [pipeline.push(self.state.fetched_data) for pipeline in self.pipelines]
        self.state.fetched_data = None
    
    def run(self):
        self.discover_data()
        self.fetch_data()
        self.pass_data()

