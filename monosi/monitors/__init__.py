from typing import Type

from monosi.monitors.base import Monitor, MonitorType
from monosi.monitors.custom import CustomMonitor
from monosi.monitors.table import TableMonitor

def load_monitor_cls(monitor_dict) -> Type[Monitor]:
    type_raw = monitor_dict.get('type')
    monitor_type = MonitorType(type_raw)

    if monitor_type == MonitorType.TABLE:
        return TableMonitor
    elif monitor_type == MonitorType.CUSTOM:
        return CustomMonitor

    # Note: Unreachable - we would error at MonitorType instantiation
    raise Exception("Could not find a moniotr with type: {}".format(type_raw))
