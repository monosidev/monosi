from argparse import ArgumentParser
import os
import sys

from .cmd.init import InitCmd
from .cmd.profile import ProfileCmd
from .cmd.run import RunCmd

# Add other modules to PYTHON_PATH
path = os.path.abspath('../')
sys.path.append(path)


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
        task = InitCmd.from_args(args)
        task.run()

    def run(self, args):
        args = None
        task = RunCmd.from_args(args)
        task.run()

    def profile(self, args):
        args = None
        task = ProfileCmd.from_args(args)
        task.run()

def get_installation_info():
    import pkg_resources

    return pkg_resources.require('monosi')[0]

def format_program_version(pkg_version, python_version):
    return u'monosi {} using Python {}\n'.format(pkg_version, python_version)

