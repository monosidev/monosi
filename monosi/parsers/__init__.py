import abc

from monosi.config.configuration import Configuration
import monosi.utils.yaml as yaml

class Parser:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    @abc.abstractmethod
    def parse_file(self, file, project):
        pass

    @property
    def default_schema(self):
        schema = self.configuration.config.schema

        return schema

    @property
    def default_database(self):
        database = self.configuration.config.database

        return database

class YamlParser(Parser):
    def __init__(self, configuration, keys):
        super().__init__(configuration)
        self.keys = keys

    def extract_from_file(self, file):
        filepath = file.filepath
        file_dict = yaml.parse_yaml(filepath)

        # TODO: Implement YAML Search
        parser_contents = file_dict
        for key in self.keys:
            parser_contents = parser_contents[key]

        return parser_contents

