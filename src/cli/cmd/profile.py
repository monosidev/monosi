from cli.config import ProjectConfiguration
from core.monitor.tasks.profile import ProfileTask
import os

from cli.utils import yaml

from .base import BaseCmd


BOOTSTRAPPED_MONITOR_PATH = './bootstrapped-monitors'

def _write_definition(definition, monitors_dir=BOOTSTRAPPED_MONITOR_PATH):
    table_parts = definition.table.split('.')
    database = table_parts[0]
    schema = table_parts[1]
    table = table_parts[2]

    monitor_path = os.path.join(monitors_dir, database, schema)
    if not os.path.exists(monitor_path):
        os.makedirs(monitor_path)

    path = os.path.join(monitor_path, table + '.yml')
    if os.path.exists(path):
        try:
            file_contents = yaml.parse_file(path)
            file_contents['monosi']['monitors'].append(definition.to_dict())
        except Exception as e:
            file_contents = {'monosi': {'monitors': definition.to_dict()}}
    else:
        file_contents = {'monosi': {'monitors': [definition.to_dict()]}}
    yaml.write_file(path, file_contents)

def _persist_definitions(definitions):
    if not os.path.exists(BOOTSTRAPPED_MONITOR_PATH):
        os.makedirs(BOOTSTRAPPED_MONITOR_PATH)

    for definition in definitions:
        _write_definition(definition)

class ProfileCmd(BaseCmd):
    def _create_tasks(self):
        sources = self.project.configuration.sources.values()

        return [ProfileTask(source) for source in sources]

    def _process_tasks(self):
        results = [task.run() for task in self.task_queue]
        for result in results:
            _persist_definitions(result)

        self.project.configuration.add_monitor_path('./bootstrapped-monitors')
        yaml.write_file(os.path.join(os.getcwd(), 'monosi_project.yml'), self.project.configuration.to_dict()) # TODO: might be yaml

        print("Profiling complete.")
