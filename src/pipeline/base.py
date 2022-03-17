from dataclasses import dataclass, field
from typing import Any, Dict, List
import json

from ingestion.job import MPipe
from pipeline.transformers.zscores import ZScoreTransformer

from .destination import MsiInternalDestination, MsiInternalDestinationConfiguration, MsiWireDestination
from .transformers.metrics import MetricTransformer


@dataclass
class MsiPipeline:
    transformers: List = field(default_factory=lambda: [MetricTransformer])
    destinations: List = field(default_factory=lambda: [])

    def _persist(self, output):
        [destination.push(output) for destination in self.destinations]

    def _transform(self, input_normalized_json):
        for transformer in self.transformers:
            if transformer.match(input_normalized_json, transformer._original_schema):
                return transformer.transform(input_normalized_json)

        return []

    def process(self, blob):
        input_normalized_json = blob
        transformed_json = self._transform(input_normalized_json)
        output_normalized_json = transformed_json

        self._persist(output_normalized_json)

def ingestion_task(source: Dict[str, Any], destination: Dict[str, Any]):
    def _create_ipipeline_zscores_dest(destination):
        dest_configuration = MsiInternalDestinationConfiguration(json.dumps(destination))
        internal_destinations = [
            MsiInternalDestination(configuration=dest_configuration)
        ]

        pipeline = MsiPipeline(
            transformers=[ZScoreTransformer],
            destinations=internal_destinations
        )

        return MsiWireDestination(pipeline=pipeline)

    def _create_ipipeline_destination(destination):
        dest_configuration = MsiInternalDestinationConfiguration(json.dumps(destination))
        internal_destinations = [
            MsiInternalDestination(configuration=dest_configuration),
            _create_ipipeline_zscores_dest(destination)
        ]

        pipeline = MsiPipeline(
            destinations=internal_destinations
        )
        wire_destination = MsiWireDestination(pipeline=pipeline)

        return wire_destination

    def _create_ipipeline(source):
        ingestion_pipeline = MPipe.from_configuration(
            sources=[source],
            destinations=[],
        )

        return ingestion_pipeline

    wire_destination = _create_ipipeline_destination(destination)
    
    ingestion_pipeline = _create_ipipeline(source)
    ingestion_pipeline.destinations = [wire_destination]

    return ingestion_pipeline
