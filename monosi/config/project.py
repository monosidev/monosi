from dataclasses import dataclass, field
import os
import glob
from typing import Any, Dict, List, Optional
from monosi.reporter import Reporter

import monosi.utils.yaml as yaml

@dataclass 
class ProjectConfigurationDefaults:
    version: str = '0.0.2.post1' # TODO: Update to automatic
    collection_name: Optional[str] = None
    source_name: Optional[str] = None
    monitor_paths: List[str] = field(default_factory=lambda: ['./monitors'])
    reporter: Reporter = field(default_factory=Reporter)
    
    @classmethod
    def _retrieve_project_config_path(cls, root_path):
        root_path = os.path.normpath(root_path)

        config_path_selector = os.path.join(root_path, 'monosi_project.y*ml')
        matches = glob.glob(config_path_selector)

        if len(matches) != 1:
            raise Exception("No project configuration file found.")

        project_config_path = matches[0]
        return project_config_path

@dataclass
class ProjectConfigurationBase:
    project_name: str
    root_path: str

@dataclass
class ProjectConfiguration(ProjectConfigurationDefaults, ProjectConfigurationBase):
    @classmethod
    def create_new(cls, project_name: str):
        root_path = os.path.abspath(os.getcwd())

        return cls(
            project_name=project_name,
            root_path=root_path,
        )

    @classmethod
    def from_root_path(cls, root_path: str) -> 'ProjectConfiguration':
        project_config_path = cls._retrieve_project_config_path(root_path)
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
        version = project_dict.get('version') or '0.0.2.post1'
        collection_name = project_dict.get('collection')
        source_name = project_dict.get('source')
        log_path: str = project_dict.get('log-path') or 'logs'

        monitor_paths: List[str] = project_dict.get('monitor-paths') or []

        project = cls(
            project_name=project_name,
            version=version,
            root_path=root_path,
            collection_name=collection_name,
            source_name=source_name,
            monitor_paths=monitor_paths,
        )

        return project

    def to_dict(self):
        config_dict = {
            "name": self.project_name,
            "version": self.version,
            "monitor-paths": self.monitor_paths,
        }
        if self.collection_name:
            config_dict.update({"collection": self.collection_name})
        if self.source_name:
            config_dict.update({"source": self.source_name})

        return config_dict


