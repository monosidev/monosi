from dataclasses import dataclass
import json


@dataclass
class IntegrationDefinition:
    name: str
    configuration: str
    enabled: bool = True

    @classmethod
    def validate(cls, monitor_dict):
        pass

    def to_dict(self):
        return {
            "name": self.name,
            "configuration": json.loads(self.configuration),
            "enabled": self.enabled,
            "type": self.__class__.__name__,
        }

    @classmethod
    def from_dict(cls, integration_dict):
        enabled = integration_dict.get('enabled') or True
        return cls(
            name=integration_dict['name'],
            enabled=enabled,
            configuration=json.dumps(integration_dict['configuration']),
        )
        
    def write(self, message):
        raise NotImplementedError()

    @classmethod
    def configuration_schema(cls):
        return {}
