from dataclasses import dataclass, field
from typing import Any, Tuple
import os

from cli.parsers.monitors import MonitorParser
from cli.utils.files import FileType, read_project_files

from core.models.project import Project
from core.models.workspace import Workspace

from .project import ProjectConfiguration
from .workspace import WorkspaceConfiguration


def parser_for_filetype(filetype: FileType):
    if filetype == FileType.MONITOR:
        return MonitorParser
    
    return None

@dataclass
class Configuration(WorkspaceConfiguration, ProjectConfiguration):
    args: Any = field(default_factory=list)

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
        workspace = WorkspaceConfiguration.from_args(args=args)

        return (project, workspace)

    @classmethod
    def from_subclasses(cls, project: ProjectConfiguration, workspace: WorkspaceConfiguration, args) -> 'Configuration':
        return cls(
            project_name=project.project_name,
            root_path=project.root_path,
            workspace_name=project.workspace_name,
            source_name=project.source_name,
            version=project.version,
            monitor_paths=project.monitor_paths,
            sources=workspace.sources,
            workspaces=workspace.workspaces,
            workspaces_dir=workspace.workspaces_dir,
            send_anonymous_stats=workspace.send_anonymous_stats,
            args=args
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

    def get_driver_config(self, source_name: str):
        if source_name not in self.sources.keys():
            raise Exception("Source {} was not defined or can not be found.")

        return self.sources[source_name]

    def to_workspace(self) -> Workspace:
        name = self.workspace_name
        send_anonymous_stats = self.send_anonymous_stats

        integrations = {}
        for source in self.workspaces[name]:
            integrations[source] = self.sources[source]

        return Workspace(
            name=name,
            integrations=integrations,
            send_anonymous_stats=send_anonymous_stats,
        )

    def validate_project(self):
        workspace_name = self.workspace_name
        source_name = self.source_name

        if workspace_name not in self.workspaces:
            raise Exception('ProjectError: Workspace {} could not be found'.format(self.workspace_name))
        elif source_name not in self.workspaces[workspace_name]:
            raise Exception('ProjectError: Source {} could not be found in workspace {}'.format(self.source_name, self.workspace_name))

        return True

    def to_project(self) -> 'Project':
        self.validate_project()

        project = Project(
            name=self.project_name,
            workspace=self.to_workspace(),
            source_name=self.source_name,
        )

        project_files = read_project_files(self)

        for filetype in project_files.keys():
            parser_cls = parser_for_filetype(filetype)

            if parser_cls:
                parser = parser_cls()

                files = project_files[filetype]
                for file in files:
                    parser.parse_file(file, project)

        return project

