from sqlalchemy.orm.session import sessionmaker

from core.models.metadata.metric import MsiMetric

class MetricsRunner:
    def __init__(self, config):
        self.config = config
        self.driver = None

    def _initialize(self):
        try:
            from core.drivers.factory import load_driver
            driver_cls = load_driver(self.config)

            self.driver = driver_cls(self.config)
        except Exception as e:
            print(e)
            raise Exception("Could not initialize connection to database in Runner.")

    def _execute(self, monitor):
        if self.driver is None:
            raise Exception("Initialize runner before execution.")

        Session = sessionmaker(self.driver.engine)
        metrics = []
        with Session() as session:
            metrics = session.query(MsiMetric).filter(
                        MsiMetric.table_name == monitor.table_name,
                        MsiMetric.database == monitor.database,
                        MsiMetric.schema == monitor.schema
                    ).all()
            session.expunge_all()
            
        return metrics

    def run(self, monitor):
        self._initialize()

        return self._execute(monitor)

# Takes object and converts to db Results
class MetricsExtractor:
    def __init__(self, source):
        self.runner = MetricsRunner(source)

    def run(self, monitor):
        results = self.runner.run(monitor)

        return results
