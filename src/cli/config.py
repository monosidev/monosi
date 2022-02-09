import os
import logging
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from core.common.drivers.base import BaseDriverConfiguration
from core.common.drivers.factory import load_config
import core.common.events as events

from cli.utils.files import file_find
import cli.utils.yaml as yaml


DEFAULT_WORKSPACES_DIR = os.path.expanduser('~/.monosi')

def read_user_id(user_filepath: str):
    user_data = yaml.parse_file(user_filepath)
    return user_data['id']

def write_user_id(user_filepath: str):
    user_id = str(uuid.uuid4())

    if not os.path.exists(user_filepath):
        user_data = {"id": user_id}
        yaml.write_file(user_filepath, user_data)

    return user_id

def convert_to_bool(val):
    if val and val.lower() == "true":
        return True
    
    return False

@dataclass
class WorkspaceConfiguration:
    sources: Dict[str, BaseDriverConfiguration] = field(default_factory=list())
    name: str = "default"
    send_anonymous_stats: bool = True
    workspaces_dir: str = DEFAULT_WORKSPACES_DIR # TODO: Update to args
    
    @classmethod
    def _config_from_source(cls, source_dict: Dict[str, Any]):
        from core.common.drivers.factory import load_config

        if 'type' not in source_dict:
            raise Exception("Source type is required.")

        driver_type = source_dict.pop('type')
        try:
            cls = load_config(driver_type)
            config = cls.from_dict(source_dict)
        except Exception as e:
            raise e

        return config

    def validate(self):
        pass

    @classmethod
    def from_dict(cls, workspace_dict: Dict[str, Any], workspace_name='default'):
        sources = {}
        if 'sources' in workspace_dict:
            for source_name in workspace_dict['sources'].keys():
                source = cls._config_from_source(workspace_dict['sources'][source_name])
                sources[source_name] = source

        config = cls(
            name=workspace_name,
            sources=sources,
        )
        config._initialize_events() # TODO: Read value

        return config

    def _initialize_events(self):
        if not self.send_anonymous_stats:
            return

        user_filepath = os.path.join(self.workspaces_dir, '.cookie.yml')
        try:
            if os.path.exists(user_filepath):
                user_id = read_user_id(user_filepath)
            else:
                user_id = write_user_id(user_filepath)
            events.set_user_id(user_id)
        except Exception as e:
            logging.error("There was an issue sending anonymous usage stats with a user id.")
        
    @classmethod
    def _get_workspace_dict(cls, workspace_name: str, all_workspaces_dict: Dict[str, Any]):
        if workspace_name not in all_workspaces_dict:
            raise Exception("Workspace not found: {}".format(workspace_name))

        return all_workspaces_dict[workspace_name]

    @classmethod
    def from_args(cls, args=None, workspace_name: str = 'default') -> 'WorkspaceConfiguration':
        try:
            workspaces_path = file_find(DEFAULT_WORKSPACES_DIR, 'workspaces.y*ml')
        except:
            raise Exception("Could not find workspaces configuration file.")

        all_workspaces_dict = yaml.parse_file(workspaces_path)
        workspace_dict = cls._get_workspace_dict(workspace_name, all_workspaces_dict)

        return cls.from_dict(workspace_dict, workspace_name)

@dataclass 
class ProjectConfiguration:
    project_name: str
    root_path: str
    workspace_name: str
    source_name: str
    version: str = '0.0.3.post2' # TODO: Pull from one location
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
        source_name = project_dict.get('source') or 'default'

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
        config_dict = {
            "name": self.project_name,
            "version": self.version,
            "monitor-paths": self.monitor_paths,
        }
        if self.workspace_name:
            config_dict.update({"workspace": self.workspace_name})
        if self.source_name:
            config_dict.update({"source": self.source_name})

        return config_dict


@dataclass
class Configuration(WorkspaceConfiguration, ProjectConfiguration):
    def __post_init__(self):
        try:
            Configuration.validate(self)
        except Exception as e:
            raise e

    @classmethod
    def validate(cls, self):
        pass

    @classmethod
    def create_subclasses(cls, args: Any) -> Tuple[ProjectConfiguration, WorkspaceConfiguration]:
        root_path = os.getcwd()
        if hasattr(args, 'project_dir'):
            root_path = args.project_dir

        project = ProjectConfiguration.from_root_path(root_path)

        workspace_name = project.workspace_name or 'default'
        workspace = WorkspaceConfiguration.from_args(
            args=args,
            workspace_name=workspace_name,
        )

        return (project, workspace)

    @classmethod
    def from_subclasses(cls, project: ProjectConfiguration, workspace: WorkspaceConfiguration, args) -> 'Configuration':
        return cls(
            project_name=project.project_name,
            version=project.version,
            root_path=project.root_path,
            monitor_paths=project.monitor_paths,
            workspace_name=project.workspace_name,
            sources=workspace.sources,
            source_name=project.source_name,
            # reporter=project.reporter,
            # config=workspace.config,
            # send_anonymous_stats=workspace.send_anonymous_stats,
            # args=args
        )

    @classmethod
    def from_args(cls, args: Any) -> 'Configuration':
        project, workspace = cls.create_subclasses(args)
        configuration = cls.from_subclasses(
            project=project,
            workspace=workspace,
            args=args
        )

        return configuration

    def project_dict(self):
        config_dict = {
            "name": self.project_name,
            "version": self.version,
            "monitor-paths": self.monitor_paths,
        }
        if self.workspace_name:
            config_dict.update({"workspace": self.workspace_name})
        if self.source_name:
            config_dict.update({"source": self.workspace_name})

        return config_dict

    def add_monitor_path(self, path):
        if path not in self.monitor_paths:
            self.monitor_paths.append(path)
            
            project_config_path = file_find(self.root_path, "monosi_project.y*ml")
            project_dict = self.project_dict()

            yaml.write_file(project_config_path, project_dict)

    def get_driver_config(self, source_name: str):
        if source_name not in self.sources.keys():
            raise Exception("Source {} was not defined or can not be found.")

        return self.sources[source_name]
