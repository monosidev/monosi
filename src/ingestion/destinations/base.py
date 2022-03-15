from dataclasses import dataclass
import abc
import json


class Publisher(object):
    def run(self, item):
        raise NotImplementedError

@dataclass
class DestinationConfiguration:
    name: str
    configuration: str
    enabled: bool = True

    def __init__(self, configuration: str):
        self.configuration = configuration

    @classmethod
    def validate(cls, configuration):
        raise NotImplementedError

    def connection_string(self):
        raise NotImplementedError

    @abc.abstractproperty
    def type(self):
        raise NotImplementedError

    def to_dict(self):
        return {
            "name": self.name,
            "configuration": json.loads(self.configuration),
            "enabled": self.enabled,
            "type": self.type,
        }

class Destination(object):
    def __init__(self, configuration):
        self.configuration = configuration

    def _before_push(self):
        pass

    def _after_push(self):
        pass

    @abc.abstractmethod
    def _push(self, data):
        raise NotImplementedError

    def push(self, data):
        self._before_push()
        results = self._push(data)
        self._after_push()

        return results
