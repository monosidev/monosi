# TODO: Runner may be responsible for loading
# the configuration for a data source based
# on the monitor definition

class Runner:
    def __init__(self, config):
        self.config = config
        self.driver = None

    def _initialize(self):
        try:
            from core.common.drivers.factory import load_driver
            driver_cls = load_driver(self.config)

            self.driver = driver_cls(self.config)
        except Exception as e:
            print(e)
            raise Exception("Could not initialize connection to database in Runner.")

    def _execute(self, sql: str):
        if self.driver is None:
            raise Exception("Initialize runner before execution.")

        results = self.driver.execute(sql)
        return results

    def run(self, sql: str):
        self._initialize()

        return self._execute(sql)
