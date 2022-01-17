from monosi.profiler import Profiler
from monosi.tasks.base import TaskBase

class ProfileTask(TaskBase):
    def run(self, *args, **kwargs):
        profiler = Profiler(self.config)
        profiler.profile()
        print("Profiling is complete.")

