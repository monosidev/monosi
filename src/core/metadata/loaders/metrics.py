# Takes SQLAlchemy objects and saves to destinations
class Loader:
    def __init__(self, destinations):
        self.destinations = destinations

    @staticmethod
    def _load(destination, metrics):
        pass

    def run(self, metrics):
        for destination in self.destinations:
            self._load(destination, metrics)
