from dataclasses import dataclass, field
from typing import List

from monosi.config.configuration import Configuration
from monosi.monitors.base import Monitor
from monosi.parsers.monitors import MonitorParser
from monosi.utils.files import FileType, read_project_files

def parser_for_filetype(filetype: FileType):
    if filetype == FileType.MONITOR:
        return MonitorParser
    
    return None

@dataclass
class Project:
    configuration: Configuration
    monitors: List[Monitor] = field(default_factory=list)

    def add_monitor(self, monitor: Monitor):
        self.monitors.append(monitor)

    @classmethod
    def from_configuration(cls, configuration: Configuration) -> 'Project':
        project = Project(configuration)
        project_files = read_project_files(configuration)

        for filetype in project_files.keys():
            parser_cls = parser_for_filetype(filetype)

            if parser_cls:
                parser = parser_cls(configuration)

                files = project_files[filetype]
                for file in files:
                    parser.parse_file(file, project)

        return project



