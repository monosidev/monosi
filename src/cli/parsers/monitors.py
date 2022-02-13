from typing import Iterable

from cli.utils.files import File

from . import YamlParser
from .definitions import MonitorDefinition


class MonitorParser(YamlParser):
    def __init__(self, configuration):
        super().__init__(configuration, ['monosi', 'monitors'])

    def parse_monitors(self, file: File) -> Iterable[MonitorDefinition]:
        monitors_dict = self.extract_from_file(file)

        for monitor_dict in monitors_dict:
            try:
                monitor = MonitorDefinition.from_dict(monitor_dict)
            except Exception as e:
                raise e
            yield monitor

    def parse_file(self, file, project):
        for monitor in self.parse_monitors(file):
            project.add_monitor(monitor)
