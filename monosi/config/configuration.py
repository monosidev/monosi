from dataclasses import dataclass
from typing import Any, Tuple
import os

import monosi.utils.yaml as yaml

from .project import ProjectConfiguration, ProjectConfigurationBase, ProjectConfigurationDefaults
from .collection import CollectionConfiguration, CollectionConfigurationBase, CollectionConfigurationDefaults

@dataclass
class ConfigurationBase(ProjectConfigurationBase, CollectionConfigurationBase):
    pass

@dataclass
class ConfigurationDefaults(ProjectConfigurationDefaults, CollectionConfigurationDefaults):
    args: Any = None

@dataclass
class Configuration(ConfigurationDefaults, ConfigurationBase):
    def __post_init__(self):
        try:
            Configuration.validate(self)
        except Exception as e:
            raise e

    @classmethod
    def validate(cls, self):
        pass

    @classmethod
    def create_subclasses(cls, args: Any) -> Tuple[ProjectConfiguration, CollectionConfiguration]:
        root_path = os.getcwd()
        if hasattr(args, 'project_dir'):
            root_path = args.project_dir

        project = ProjectConfiguration.from_root_path(root_path)

        collection_name = (project.collection_name or 'default')
        source_name = (project.source_name or 'default')
        collection = CollectionConfiguration.from_args(
            collection_name=collection_name, 
            source_name=source_name,
            args=args
        )

        return (project, collection)

    @classmethod
    def from_subclasses(cls, project: ProjectConfiguration, collection: CollectionConfiguration, args) -> 'Configuration':
        return cls(
            project_name=project.project_name,
            version=project.version,
            root_path=project.root_path,
            monitor_paths=project.monitor_paths,
            collection_name=project.collection_name,
            source_name=project.source_name,
            reporter=project.reporter,
            config=collection.config,
            send_anonymous_stats=collection.send_anonymous_stats,
            args=args)

    @classmethod
    def from_args(cls, args: Any) -> 'Configuration':
        project, collection = cls.create_subclasses(args)
        configuration = cls.from_subclasses(
            project=project,
            collection=collection,
            args=args
        )

        return configuration

    def project_dict(self):
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

    def add_monitor_path(self, path):
        if path not in self.monitor_paths:
            self.monitor_paths.append(path)
            
            project_config_path = self._retrieve_project_config_path(self.root_path)
            project_dict = self.project_dict()

            yaml.write_file(project_config_path, project_dict)
