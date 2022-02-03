from typing import Iterable

from core.monitor.models import MonitorDefinition
from core.monitor.models.custom import CustomMonitorDefinition
from core.monitor.models.schema import SchemaMonitorDefinition
from core.monitor.models.table import TableMonitorDefinition
from cli.utils.files import File

from . import YamlParser

# TODO: Replace with configuration object
def monitor_definition_factory(monitor_dict):
    monitor_type = monitor_dict['type'].lower()
    if monitor_type == 'table':
        return TableMonitorDefinition
    elif monitor_type == 'custom':
        return CustomMonitorDefinition
    elif monitor_type == 'schema':
        return SchemaMonitorDefinition

    raise Exception("Could not find monitor type: {}".format(monitor_type))

class MonitorParser(YamlParser):
    def __init__(self, configuration):
        super().__init__(configuration, ['monosi', 'monitors'])

    def parse_monitors(self, file: File) -> Iterable[MonitorDefinition]:
        monitors_dict = self.extract_from_file(file)

        for monitor_dict in monitors_dict:
            try:
                monitor_def_class = monitor_definition_factory(monitor_dict)
                monitor_def_class.validate(monitor_dict)
                monitor = monitor_def_class.from_dict(monitor_dict)
            except Exception as e:
                raise e
            yield monitor

    def parse_file(self, file, project):
        for monitor in self.parse_monitors(file):
            project.add_monitor(monitor)
