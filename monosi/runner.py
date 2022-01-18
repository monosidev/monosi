from monosi.analyzer import Analyzer
from monosi.config.configuration import Configuration
from monosi.compiler import Compiler
from monosi.events import track_event

class Runner:
    def __init__(self, config: Configuration, monitors):
        self.config = config
        self.monitors = monitors
        self.driver = None

    def _initialize(self):
        try:
            from monosi.drivers.factory import load_driver
            driver_config = self.config.config
            driver_cls = load_driver(driver_config)

            self.driver = driver_cls(self.config)
        except:
            raise Exception("Could not initialize connection to database in runner.")

    def get_compiler(self):
        if self.driver is None:
            raise Exception("Initialize runner before compilation")

        metadata = self.driver.metadata()

        return Compiler(self.driver.dialect, metadata)

    def execute(self, sql: str):
        if self.driver is None:
            raise Exception("Initialize runner before execution.")

        results = self.driver.execute_sql(sql)
        return results

    def run(self):
        self._initialize()

        reporter = self.config.reporter
        compiler = self.get_compiler()
        analyzer = Analyzer(reporter)

        for monitor in self.monitors:
            reporter.monitor_started(monitor)
            try:

                sql_stmt = compiler.compile(monitor)
                results = self.execute(sql_stmt)

                analyzer.analyze(monitor, results)
            finally:
                reporter.monitor_finished(monitor)
                
        # reporter.finish()

