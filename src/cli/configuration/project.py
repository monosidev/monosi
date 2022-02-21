from dataclasses import dataclass, field
from typing import Any, Dict, List

from cli.utils.files import file_find
import cli.utils.yaml as yaml

@dataclass 
class ProjectConfiguration:
    project_name: str
    root_path: str
    workspace_name: str
    source_name: str
    version: str = '0.0.3' # TODO: Pull from one location
    monitor_paths: List[str] = field(default_factory=lambda: ['./monitors'])
    
    @classmethod
    def from_root_path(cls, root_path: str) -> 'ProjectConfiguration':
        project_config_path = file_find(root_path, 'monosi_project.y*ml')
        project_dict = yaml.parse_file(project_config_path)

        return cls.from_dict(
            root_path=root_path,
            project_dict=project_dict,
        )

    @classmethod
    def validate(cls, project_dict):
        pass

    @classmethod
    def from_dict(
        cls,
        root_path: str,
        project_dict: Dict[str, Any],
    ):
        try:
            cls.validate(project_dict)
        except Exception as e:
            raise e

        project_name = str(project_dict.get('name'))
        version = project_dict.get('version') or '0.0.3'
        workspace_name = project_dict.get('workspace') or 'default'
        source_name = project_dict.get('source')  or 'default'

        monitor_paths: List[str] = project_dict.get('monitor-paths') or []

        project = cls(
            project_name=project_name,
            version=version,
            root_path=root_path,
            workspace_name=workspace_name,
            source_name=source_name,
            monitor_paths=monitor_paths,
        )

        return project

    def to_dict(self):
        return {
            "name": self.project_name,
            "version": self.version,
            "monitor-paths": self.monitor_paths,
            "source": self.source_name,
            "workspace": self.workspace_name,
        }

