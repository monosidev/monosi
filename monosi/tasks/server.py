from monosi.server import create_app
from monosi.tasks.base import ProjectTask, TaskBase

class StartServerTask(TaskBase):
    def run(self, *args, **kwargs):
        app = create_app()
        app.run()

class ServerTask(ProjectTask):
    def run(self, *args, **kwargs):
        start_server = StartServerTask(args, kwargs)
        start_server.run()
