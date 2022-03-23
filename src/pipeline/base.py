from dataclasses import dataclass, field
from typing import Any, Dict, List
import json

from ingestion.job import MPipe

from .source import MsiInternalSource, MsiInternalSourceConfiguration
from .transformers import AnomalyTransformer, MonitorTransformer, MetricTransformer, ZScoreTransformer
from .destination import MsiIntegrationDestination, MsiInternalDestination, MsiInternalDestinationConfiguration, MsiWireDestination


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


# ZScores Task & Alerting
def analysis_task(source: Dict[str, Any], destination: Dict[str, Any], alerts):
    def _create_ipipeline_zscores_dest(destination, alerts):
        def _create_ipipeline_alerts_dest(alerts):
            pipeline = MsiPipeline(
                transformers=[AnomalyTransformer],
                destinations=[MsiIntegrationDestination(alert) for alert in alerts],
            )
            wire_destination = MsiWireDestination(pipeline=pipeline)

            return wire_destination

        dest_configuration = MsiInternalDestinationConfiguration(json.dumps(destination))
        internal_destinations = [
            MsiInternalDestination(configuration=dest_configuration),
            _create_ipipeline_alerts_dest(alerts),
        ]

        pipeline = MsiPipeline(
            transformers=[ZScoreTransformer],
            destinations=internal_destinations
        )
        wire_destination = MsiWireDestination(pipeline=pipeline)

        return wire_destination

    def _create_ipipeline_source(source_dict):
        source_config = MsiInternalSourceConfiguration(
            name=None,
            configuration=json.dumps(source_dict)
        )
        source = MsiInternalSource(source_config)

        return source


    metrics_source = _create_ipipeline_source(source)
    wire_destination_zscores = _create_ipipeline_zscores_dest(destination, alerts)
    
    ingestion_pipeline = MPipe(sources=[], destinations=[])
    ingestion_pipeline.sources = [metrics_source]
    ingestion_pipeline.destinations = [wire_destination_zscores]

    return ingestion_pipeline


# Table Health Metrics Collection Task
def ingestion_task(source: Dict[str, Any], destination: Dict[str, Any]):
    def _create_ipipeline_destination_monitors(destination):
        dest_configuration = MsiInternalDestinationConfiguration(json.dumps(destination))
        internal_destinations = [
            MsiInternalDestination(configuration=dest_configuration),
        ]

        pipeline = MsiPipeline(
            destinations=internal_destinations,
            transformers=[MonitorTransformer],
        )
        wire_destination = MsiWireDestination(pipeline=pipeline)

        return wire_destination

    def _create_ipipeline_destination(destination):
        dest_configuration = MsiInternalDestinationConfiguration(json.dumps(destination))
        internal_destinations = [
            MsiInternalDestination(configuration=dest_configuration),
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

    wire_destination_metrics = _create_ipipeline_destination(destination)
    wire_destination_monitors = _create_ipipeline_destination_monitors(destination)
    
    ingestion_pipeline = _create_ipipeline(source)
    ingestion_pipeline.destinations = [wire_destination_metrics, wire_destination_monitors]

    return ingestion_pipeline
