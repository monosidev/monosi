import logging
from core.common.reporter import reporter

class RunMonitorTask:
    def __init__(self, monitor):
        self.monitor = monitor
        self.reporter = reporter

    # def _retrieve_driver_config(self):
    #     try:
    #         from core.common.drivers.factory import load_driver_config
    #         driver_config = self.monitor.driver_config
    #         driver_config_cls = load_driver_config(driver_config)

    #         return driver_config_cls(self.config)
    #     except:
    #         raise Exception("Could not initialize connection to database in runner.")

    def _retrieve_driver_config(self):
        return self.monitor.driver_config

    def _compile(self):
        from core.monitor.compiler import Compiler

        compiler = Compiler(self._retrieve_driver_config())
        return compiler.compile(self.monitor)

    def _run(self, sql):
        from core.monitor.runner import Runner

        runner = Runner(self._retrieve_driver_config())
        return runner.run(sql)

    def _analyze(self, results):
        from core.monitor.analyzer import Analyzer
        
        analyzer = Analyzer(self.reporter)
        return analyzer.analyze(self.monitor, results)

    def run(self):
        self.reporter.monitor_started(self.monitor)

        runner_results = None
        try:
            compiled_sql = self._compile()
            runner_results = self._run(compiled_sql)
            analysis = self._analyze(runner_results)
        except:
            logging.error("There was an issue running the monitor.")

        self.reporter.monitor_finished(self.monitor)

        return runner_results

        # return (runner_results, analysis)

# class RunAllMonitorsTask:
#     def __init__(self, monitors):
#         self.monitors = monitors

#     def _create_tasks(self):
#         return self.monitors

#     @staticmethod
#     def _process_tasks(tasks):
#         tasks = self._create_tasks()
#         return [task.run() for task in tasks]
    
#     def run(self):
#         return self._process_tasks()
