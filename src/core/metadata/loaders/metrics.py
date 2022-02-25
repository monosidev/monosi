from sqlalchemy.orm import sessionmaker

from core.models import mapper_registry

# Takes SQLAlchemy objects and saves to destinations
class Loader:
    def __init__(self, destinations):
        self.destinations = destinations

    @staticmethod
    def _load(destination, metrics):
        from core.drivers.factory import load_driver

        driver_cls = load_driver(destination)
        driver = driver_cls(destination)

        driver._before_execute()
        mapper_registry.metadata.create_all(driver.engine)

        print(driver.engine)
        Session = sessionmaker(bind=driver.engine)
        with Session() as session:
            from core.models.metadata.metric import MsiMetric
            session.bulk_insert_mappings(MsiMetric, [metric.to_dict() for metric in metrics])
            session.commit()
            session.close()

    def run(self, metrics):
        for destination in self.destinations:
            self._load(destination, metrics)
