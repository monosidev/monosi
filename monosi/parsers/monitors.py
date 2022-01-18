from typing import Iterable

from monosi.monitors import load_monitor_cls
from monosi.monitors.base import Monitor
from monosi.parsers import YamlParser
from monosi.utils.files import File

class MonitorParser(YamlParser):
    def __init__(self, configuration):
        super().__init__(configuration, ['monosi', 'monitors'])

    def _fqtablename(self, table):
        table_parts = table.split('.')
        
        if len(table_parts) > 3:
            raise Exception("Can't resolve table name: {}".format(table))
        
        if len(table_parts) == 1 and self.default_schema:
            table_parts.insert(0, self.default_schema)
        if len(table_parts) == 2 and self.default_database:
            table_parts.insert(0, self.default_database)

        return ".".join(table_parts)

    def _resolve_table(self, monitor_dict):
        if 'type' not in monitor_dict or monitor_dict['type'] != 'table':
            return

        fqn = self._fqtablename(monitor_dict['table'])
        monitor_dict['table'] = fqn

    def parse_monitors(self, file: File) -> Iterable[Monitor]:
        monitors_dict = self.extract_from_file(file)

        for monitor_dict in monitors_dict:
            try:
                monitor_cls = load_monitor_cls(monitor_dict)
                monitor_cls.validate(monitor_dict)
                self._resolve_table(monitor_dict)
                monitor = monitor_cls.from_dict(monitor_dict)
            except Exception as e:
                raise e
            yield monitor

    def parse_file(self, file, project):
        for monitor in self.parse_monitors(file):
            project.add_monitor(monitor)

