from monosi.server import create_app
from monosi.tasks.base import TaskBase

class ServerTask(TaskBase):
    def run(self, *args, **kwargs):
        app = create_app()
        app.run()

