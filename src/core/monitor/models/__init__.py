from dataclasses import dataclass, field
from enum import Enum
from typing import Optional 
import json

from .schedule import Schedule, ScheduleType

def load_monitor_cls(monitor_dict):
    monitor_type = monitor_dict.get('type').lower()
    # monitor_type = MonitorType(type_raw)

    if monitor_type == "table":
        from .table import TableMonitor
        return TableMonitor
    elif monitor_type == "custom":
        from .custom import CustomMonitor
        return CustomMonitor
    elif monitor_type == "schema":
        from .schema import SchemaMonitor
        return SchemaMonitor

    raise Exception("Could not find a moniotr with type: {}".format(monitor_type))

def load_monitor_definition(monitor_definition):
    monitor_type = monitor_definition['type']
    # monitor_type = MonitorType(type_raw)

    configuration = monitor_definition['configuration']
    if monitor_type == "table":
        from .table import TableMonitorDefinition
        # TableMonitorDefinition.validate()
        return TableMonitorDefinition(
            **monitor_definition,
            **configuration,
        )
    elif monitor_type == "custom":
        from .custom import CustomMonitorDefinition
        # CustomMonitorDefinition.validate()
        return CustomMonitorDefinition(
            **monitor_definition,
            **configuration,
        )
    elif monitor_type == "schema":
        from .schema import SchemaMonitorDefinition
        # SchemaMonitorDefinition.validate()
        return SchemaMonitorDefinition(
            **monitor_definition,
            **configuration,
        )

    # Note: Unreachable - we would error at MonitorType instantiation
    raise Exception("Could not find a monitor definition with type: {}".format(monitor_type))

@dataclass
class MonitorConfiguration:
    pass

# TODO: It's likely that a monitor definition
# will have to include information about which
# datasource it is intended to run on and a
# way to grab its configuration information
@dataclass
class MonitorDefinition:
    name: str
    type: str
    # workspace: str
    configuration: str # TODO (This is NOT a connection configuration, it is the details for the individ monitor)
    schedule_minutes: int = 720
    schedule_type: str = ScheduleType.INTERVAL._value_
    datasource: str = 'default' # Used (with workspace) to resolve the DriverConfig
    description: Optional[str] = None
    enabled: Optional[bool] = True
    # schedule: Schedule = field(default_factory=lambda: Schedule())

    @classmethod
    def validate(cls, monitor_dict):
        pass

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "type": self.type,
            "datasource": self.datasource,
            # "schedule": Schedule(self.schedule_minutes).to_dict(),
            "schedule_minutes": self.schedule_minutes,
            "schedule_type": self.schedule_type,
            "configuration": json.loads(self.configuration),
        }

    @classmethod
    def from_dict(cls, monitor_dict):
        if 'configuration' in monitor_dict:
            configuration = json.dumps(monitor_dict['configuration'])
            monitor_dict['configuration'] = configuration
        else:
            monitor_dict['configuration'] = '{}'

        return cls(
            **monitor_dict,
        )

    def to_monitor(self, workspace): # TODO: to_dict contains id, updated_at, created_at
        monitor_dict = self.to_dict()
        monitor_dict.pop('id')
        try:
            monitor_dict.pop('last_run')
        except:
            pass
        monitor_dict.pop('created_at')
        monitor_dict.pop('updated_at')
        monitor_cls = load_monitor_definition(monitor_dict)
        return monitor_cls.to_monitor(workspace)

