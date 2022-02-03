from dataclasses import dataclass
from enum import Enum

class ScheduleType(Enum):
    INTERVAL = 'interval'

@dataclass
class Schedule:
    minutes: int = 720
    type: ScheduleType = ScheduleType.INTERVAL

    def to_dict(self):
        return {
            "minutes": self.minutes,
            "type": self.type._value_,
        }
