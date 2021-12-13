from typing import Type

from monosi.monitors.base import Monitor, MonitorType
from monosi.monitors.table_metrics import TableMetricsMonitor

def load_monitor_cls(monitor_dict) -> Type[Monitor]:
    type_raw = monitor_dict.get('type')
    monitor_type = MonitorType(type_raw)

    if monitor_type == MonitorType.TableMetrics:
        return TableMetricsMonitor

    return Monitor

