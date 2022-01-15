from dataclasses import dataclass
from enum import Enum

class MetricType(Enum):
    CUSTOM = 'custom'

@dataclass
class MetricBase:
    type: MetricType

    def alias(self):
        return self.type._value_

