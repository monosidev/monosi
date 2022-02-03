import abc
from dataclasses import dataclass
from enum import Enum

from core.common.drivers.base import BaseDialect

class MetricType(Enum):
    CUSTOM = 'custom'

@dataclass
class MetricBase:
    type: MetricType

    def alias(self):
        return self.type._value_

    @abc.abstractmethod
    def compile(self, dialect: BaseDialect):
        raise NotImplementedError

