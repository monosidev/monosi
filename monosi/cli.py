import os
import sys
from argparse import ArgumentParser
from monosi.config.project import ProjectConfiguration

from monosi.jobs.run import MonitorsJob
from monosi.utils.yaml import write_file

class CliParser(object):
    """Argument parser for the CLI"""

    def __init__(self):
        self._parser = ArgumentParser()
        self._add_arguments()

    def _add_arguments(self):
        """Adds arguments to parser."""
        self._parser.add_argument(
            '-v', '--version',
            action='version', 
            version=self.version(),
            help='Show the version number.'
        )
        self._parser.add_argument('-c','--command', help='Subcommand to run')

    def parse(self, argv):
        args = self._parser.parse_args(argv[1:])
        getattr(self, args.command)()
        
    # Commands
    def version(self):
        return format_program_version(get_installation_info().version, sys.version.split()[0])

    def init(self):
        project_name = "project"
        project_configuration = ProjectConfiguration.create_new(project_name)

        project_directory = os.path.join(os.getcwd(), project_name)
        os.mkdir(project_directory)

        project_file = os.path.join(project_directory, 'monosi_project.yml')
        write_file(project_file, project_configuration.to_dict())

        print("Successfully initialized monosi project.")

    def profile(self):
        print("This profiles the existing configuration for monitors you may want to set.")

    def run(self):
        args = None
        job = MonitorsJob.from_args(args)
        job.run()

def get_installation_info():
    import pkg_resources

    return pkg_resources.require('monosi')[0]

def format_program_version(pkg_version, python_version):
    return u'monosi {} using Python {}\n'.format(pkg_version, python_version)

