from .base import ProjectCmd
from core.metadata.task import RunMonitorsTask


class RunCmd(ProjectCmd):
    def _process(self):
        if self.project == None:
            raise Exception("Could not initialize the project to run the monitors.")

        source = self.project.source_name
        destinations = self.project.source_name

        task = RunMonitorsTask.from_source_and_destinations(
            self.project.monitors,
            source,
            destinations,
        )
        return task.run()
