import abc

from cli.configuration import Configuration


class BaseCmd:
    def __init__(self, args, config):
        self.args = args
        self.config = config

    @classmethod
    def from_args(cls, args):
        try:
            config = Configuration.from_args(args)
        except:
            raise Exception("There was an issue creating the task from args.")

        return cls(args, config)

    @classmethod
    def run_task(cls, *args, **kwargs):
        task = cls(*args)
        return task.run(*args, **kwargs)

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError('Implementation for task does not exist.')

class ProjectCmd(BaseCmd):
    def __init__(self, args, config):
        super().__init__(args, config)
        self.project = None

    def load_project(self):
        self.project = self.config.to_project()

    def _initialize(self):
        self.load_project()

    @abc.abstractmethod
    def _process(self):
        raise NotImplementedError

    def run(self):
        self._initialize()
        return self._process()

