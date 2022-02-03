from dataclasses import dataclass, field
from typing import List

from core.monitor.models import MonitorDefinition

from .config import Configuration
from .parsers.monitors import MonitorParser
from .utils.files import FileType, read_project_files

def parser_for_filetype(filetype: FileType):
    if filetype == FileType.MONITOR:
        return MonitorParser
    
    return None

@dataclass
class Project:
    configuration: Configuration
    monitors: List[MonitorDefinition] = field(default_factory=list)

    def add_monitor(self, monitor: MonitorDefinition):
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
