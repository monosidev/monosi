from dataclasses import dataclass, field
from typing import Any, Dict, List
import itertools

from .destinations import Destination, DestinationFactory
from .sources import Source, SourceFactory
from .task import Task


def flatten(arr):
    return list(itertools.chain.from_iterable(arr))

@dataclass
class MPipe:
    sources: List[Source]
    destinations: List[Destination]
    tasks: List[Task] = field(default_factory=list)

    @classmethod
    def from_configuration(cls, sources: List[Dict[str, Any]], destinations: List[Dict[str, Any]]):
        source_objs = [SourceFactory.create(configuration) for configuration in sources]
        destination_objs = [DestinationFactory.create(configuration) for configuration in destinations]

        return MPipe(sources=source_objs, destinations=destination_objs)

    def _create_source_tasks(self, source: Source):
        extractor = source.extractor()
        task_units = source.task_units()

        return [Task(extractor=extractor, units=[unit]) for unit in task_units]

    def _create_tasks(self):
        self.tasks = flatten([self._create_source_tasks(source) for source in self.sources])

    def publish(self, data):
        return [destination.push(data) for destination in self.destinations]

    def run(self):
        # Create Tasks
        self._create_tasks()

        # Run tasks
        for task in self.tasks:
            task_results = task.run()
            while True:
                try:
                    units_result = next(task_results)
                    
                    while True:
                        try:
                            unit_results = next(units_result)
                            self.publish([[[unit_results]]])
                        except StopIteration:
                            break
                except StopIteration:
                    break

        
        # # Publish results
        # self.publish(results)

