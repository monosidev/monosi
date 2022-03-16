from typing import Any, Dict, Type
import json

from .base import (
    Extractor,
	Source,
    SourceConfiguration,
)

from .postgresql import PostgreSQLSource, PostgreSQLSourceConfiguration
from .snowflake import SnowflakeSource, SnowflakeSourceConfiguration

class SourceFactory:
    @classmethod
    def _configuration_cls(cls, config_type: str) -> Type[SourceConfiguration]:
        if config_type.lower() == 'postgresql':
            return PostgreSQLSourceConfiguration
        elif config_type == 'snowflake':
            return SnowflakeSourceConfiguration
        else:
            raise Exception("Error: Unknown source type.")

    @classmethod
    def _source_cls(cls, config_type: str) -> Type[Source]:
        if config_type.lower() == 'postgresql':
            return PostgreSQLSource
        elif config_type.lower() == 'snowflake':
            return SnowflakeSource
        else:
            raise Exception("Error: Unknown source type.")

    @classmethod
    def create(cls, configuration: Dict[str, Any]) -> Source:
        config_type = configuration.get('type')
        if config_type == None:
            raise Exception("Error: No source type set.")

        configuration_cls = cls._configuration_cls(config_type)
        source_cls = cls._source_cls(config_type)

        configuration_obj = configuration_cls(name=None, configuration=json.dumps(configuration))
        destination = source_cls(configuration_obj)

        return destination

