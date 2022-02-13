import os
import logging
import uuid

from dataclasses import dataclass, field
from typing import Any, Dict, List

from core.drivers.base import BaseDriverConfiguration

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

@dataclass
class WorkspaceConfiguration:
    workspaces: Dict[str, List[str]] = field(default_factory=dict)
    sources: Dict[str, BaseDriverConfiguration] = field(default_factory=dict)
    workspaces_dir: str = DEFAULT_WORKSPACES_DIR # TODO: Update to args
    send_anonymous_stats: bool = True
    
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

    @classmethod
    def validate(cls, workspace_dict):
        pass

    @classmethod
    def from_dict(cls, workspace_dict: Dict[str, Any]):
        cls.validate(workspace_dict)

        workspaces = {}
        for name in workspace_dict:
            workspaces[name] = [source for source in workspace_dict[name]]

        sources = {}
        for ws_name in workspaces:
            source_names = workspaces[ws_name]
            for source_name in source_names:
                source = cls._config_from_source(workspace_dict[ws_name]['sources'][source_name])
                sources[source_name] = source
            if 'sources' in workspace_dict:
                for source_name in workspace_dict['sources'].keys():
                    source = cls._config_from_source(workspace_dict['sources'][source_name])
                    sources[source_name] = source

        send_anonymous_stats = bool(workspace_dict.get('send_anonymous_stats') or True)

        config = cls(
            workspaces=workspaces,
            sources=sources,
            send_anonymous_stats=send_anonymous_stats,
        )
        config._initialize_events()

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
            # events.set_user_id(user_id)
        except Exception as e:
            logging.error("There was an issue sending anonymous usage stats with a user id.")

    @classmethod
    def from_args(cls, args=None) -> 'WorkspaceConfiguration':
        try:
            workspaces_path = file_find(DEFAULT_WORKSPACES_DIR, 'workspaces.y*ml')
        except:
            raise Exception("Could not find workspaces configuration file.")

        workspaces_dict = yaml.parse_file(workspaces_path)

        return cls.from_dict(workspaces_dict)
