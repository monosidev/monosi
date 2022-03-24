from typing import Any, Dict, Type
import logging
import json

from .base import (
    Destination,
    DestinationConfiguration
)
from .monosi import MonosiDestination, MonosiDestinationConfiguration


class DestinationFactory:
    @classmethod
    def _configuration_cls(cls, config_type: str) -> Type[DestinationConfiguration]:
        config_type = config_type.lower()
        if config_type == "monosi":
            return MonosiDestinationConfiguration
        else:
            raise Exception("Error: Unknown destination type.")

    @classmethod
    def _destination_cls(cls, config_type: str) -> Type[Destination]:
        config_type == config_type.lower()
        if config_type == "monosi":
            return MonosiDestination
        else:
            raise Exception("Error: Unknown destination type.")

    @classmethod
    def create(cls, configuration: Dict[str, Any]) -> Destination:
        config_type = configuration.get('type')
        if config_type == None:
            raise Exception("Error: No destination type set.")

        configuration_cls = cls._configuration_cls(config_type)
        destination_cls = cls._destination_cls(config_type)

        configuration_obj = configuration_cls(
            configuration=json.dumps(configuration)
        )
        destination = destination_cls(configuration_obj)

        return destination

