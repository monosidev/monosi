from dataclasses import dataclass, field
from typing import Any, Dict, List, Type

from .destinations import Destination, DestinationFactory
from .transformers import Transformer


@dataclass
class Pipeline(Destination):
    transformers: List[Type[Transformer]]
    destinations: List[Destination]

    @classmethod
    def from_configuration(cls, transformers: List[Type[Transformer]] = [], destinations: List[Dict[str, Any]] = []):
        destination_objs = [DestinationFactory.create(configuration) for configuration in destinations]

        return Pipeline(transformers=transformers, destinations=destination_objs)

    def _transform(self, input_normalized_json):
        for transformer in self.transformers:
            if transformer.match(input_normalized_json, transformer._original_schema()):
                return transformer.transform(input_normalized_json)

        return input_normalized_json

    def publish(self, data):
        return [destination.push(data) for destination in self.destinations]

    def _push(self, input_dict):
        transformed_dict = self._transform(input_dict)
        # output_normalized_json = transformed_dict
        self.publish(transformed_dict)


