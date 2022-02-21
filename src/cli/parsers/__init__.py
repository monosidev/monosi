import abc

import cli.utils.yaml as yaml


class Parser(object):
    @abc.abstractmethod
    def parse_file(self, file, project):
        pass

class YamlParser(Parser):
    def __init__(self, keys):
        self.keys = keys

    def extract_from_file(self, file):
        filepath = file.filepath
        file_dict = yaml.parse_yaml(filepath)

        # TODO: Implement YAML Search
        parser_contents = file_dict
        for key in self.keys:
            parser_contents = parser_contents[key]

        return parser_contents
