import os
import sys
from argparse import ArgumentParser
from monosi.config.project import ProjectConfiguration

from monosi.tasks.profile import ProfileTask
from monosi.tasks.run import RunMonitorsTask
from monosi.tasks.server import ServerTask
from monosi.utils.yaml import write_file

class CliParser(object):
    """Argument parser for the CLI"""

    def __init__(self):
        self._parser = ArgumentParser()
        self._add_arguments()

    def _add_arguments(self):
        """Adds arguments to parser."""
        self._parser.add_argument(
            'command', type=str
        )
        self._parser.add_argument(
            '-v', '--version',
            action='version', 
            version=self.version(),
            help='Show the version number.'
        )

    def parse(self, argv):
        args = self._parser.parse_args(argv[1:])
        getattr(self, args.command)(argv[1:])
        
    # Commands
    def version(self, args=None):
        return format_program_version(get_installation_info().version, sys.version.split()[0])

    def init(self, args):
        args = None
        project_name = "project"
        project_configuration = ProjectConfiguration.create_new(project_name)

        project_directory = os.path.join(os.getcwd(), project_name)
        os.mkdir(project_directory)

        project_file = os.path.join(project_directory, 'monosi_project.yml')
        write_file(project_file, project_configuration.to_dict())

        print("Successfully initialized monosi project.")

    def profile(self, args):
        args = None
        task = ProfileTask.from_args(args)
        task.run()

    def run(self, args):
        args = None
        task = RunMonitorsTask.from_args(args)
        task.run()

    def server(self, args):
        args = None
        task = ServerTask.from_args(args)
        task.run()

def get_installation_info():
    import pkg_resources

    return pkg_resources.require('monosi')[0]

def format_program_version(pkg_version, python_version):
    return u'monosi {} using Python {}\n'.format(pkg_version, python_version)

