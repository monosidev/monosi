from dataclasses import dataclass, field
from typing import Any, Dict, List, Type
import itertools

from .destinations import Destination, DestinationFactory
from .sources import Source, SourceFactory
from .transformers import Transformer
from .task import Task


def flatten(arr):
    return list(itertools.chain.from_iterable(arr))

@dataclass
class Pipe(Destination):
    sources: List[Source]
    transformers: List[Type[Transformer]]
    destinations: List[Destination]

    @classmethod
    def from_configuration(cls, sources: List[Dict[str, Any]] = [], destinations: List[Dict[str, Any]] = [], transformers: List[Type[Transformer]] = []):
        source_objs = [SourceFactory.create(configuration) for configuration in sources]
        destination_objs = [DestinationFactory.create(configuration) for configuration in destinations]

        return Pipe(sources=source_objs, transformers=transformers, destinations=destination_objs)

    def _transform(self, input_normalized_json):
        for transformer in self.transformers:
            if transformer.match(input_normalized_json, transformer._original_schema()):
                return transformer.transform(input_normalized_json)

        return input_normalized_json

    def _create_source_tasks(self, source: Source):
        extractor = source.extractor()
        task_units = source.task_units()

        return [Task(extractor=extractor, units=[unit]) for unit in task_units]

    def _create_tasks(self):
        return flatten([self._create_source_tasks(source) for source in self.sources])

    def publish(self, data):
        return [destination.push(data) for destination in self.destinations]

    def _push(self, input_dict):
        transformed_dict = self._transform(input_dict)
        # output_normalized_json = transformed_dict
        self.publish(transformed_dict)


