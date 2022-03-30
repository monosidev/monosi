from dataclasses import dataclass
from enum import Enum
import itertools
from typing import Any, Dict, List, Optional

from mashumaro.serializer.base.dict import DataClassDictMixin
from ingestion.sources import SourceFactory

from ingestion.sources.base import Source
from ingestion.task import Task

from .pipeline import Pipeline


class MonitorType(Enum):
    SCHEMA = 'schema'
    TABLE = 'table'

@dataclass
class Monitor(DataClassDictMixin):
    type: str
    definition: Optional[Dict] = None

@dataclass
class CollectorConfiguration(DataClassDictMixin): # This is technically repr of what YAML used to be
    monitors: List[Monitor]

    @classmethod
    def default(cls):
        return cls(monitors=[])

@dataclass
class Collector:
    source: Source
    pipelines: List[Pipeline]
    configuration: CollectorConfiguration = CollectorConfiguration.default()

    def _create_tasks(self, discovered_data):
        extractor = self.source.extractor()
        task_units = self.source.task_units(discovered_data, self.configuration.monitors)

        return [Task(extractor=extractor, units=[unit]) for unit in task_units]

    @classmethod
    def from_configuration(cls, source_dict: Dict[str, Any], pipelines = [], configuration = {'monitors': []}):
        source = SourceFactory.create(source_dict)
        configuration = CollectorConfiguration.from_dict(configuration)

        return cls(source=source, pipelines=pipelines, configuration=configuration)

    def discover_data(self):
        discovery_query = self.source.discovery_query()
        extractor = self.source.extractor()

        return extractor.run(discovery_query)

    def fetch_data(self, discovered_data):
        # Run tasks
        for task in self._create_tasks(discovered_data):
            task_results_gen = task.run()
            while True:
                try:
                    units_results_gen = next(task_results_gen)
                    
                    while True:
                        try:
                            fetched_data = next(units_results_gen)
                            self.pass_data(fetched_data)
                        except StopIteration:
                            break
                except StopIteration:
                    break

    def pass_data(self, data):
        try:
            [pipeline.push(data) for pipeline in self.pipelines]
        except Exception as e:
            print(e)

    # def _create_tasks(self):
    #     extractor = self.source.extractor()
    #     task_units = self.source.task_units(self.configuration)

    #     return [Task(extractor=extractor, units=[unit]) for unit in task_units]

    # def fetch_and_send_data(self):
    #     # Run tasks
    #     for task in self._create_tasks():
    #         task_results_gen = task.run()
    #         while True:
    #             try:
    #                 units_results_gen = next(task_results_gen)
                    
    #                 while True:
    #                     try:
    #                         fetched_data = next(units_results_gen)
    #                         self.pass_data(fetched_data)
    #                     except StopIteration:
    #                         break
    #             except StopIteration:
    #                 break
    
    # def run(self):
    #     self.fetch_and_send_data()

    def run(self):
        discovered_data = self.discover_data() # TODO: Move Discover, Fetch, Return to tasks, create from monitor def
        data = self.fetch_data(discovered_data)
        self.pass_data(data)

