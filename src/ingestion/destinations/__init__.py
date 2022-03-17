from typing import Any, Dict, Type

from .base import (
    Destination,
    DestinationConfiguration,
    Publisher,
)

class DestinationFactory:
    @classmethod
    def _configuration_cls(cls, config_type: str) -> Type[DestinationConfiguration]:
        if False:
            return
        else:
            raise Exception("Error: Unknown destination type.")

    @classmethod
    def _destination_cls(cls, config_type: str) -> Type[Destination]:
        if False:
            return
        else:
            raise Exception("Error: Unknown destination type.")

    @classmethod
    def create(cls, configuration: Dict[str, Any]) -> Destination:
        print(configuration)
        config_type = configuration.get('type')
        if config_type == None:
            raise Exception("Error: No destination type set.")

        configuration_cls = cls._configuration_cls(config_type)
        destination_cls = cls._destination_cls(config_type)

        configuration_obj = configuration_cls(name=None, configuration=str(configuration))
        destination = destination_cls(configuration_obj)

        return destination
