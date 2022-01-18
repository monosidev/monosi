import os
from flask import Flask
from flask_cors import CORS

from monosi.scheduler.manager import JobManager
from monosi.tasks.schedule import ScheduleMonitorsTask

def load_monitors(app):
    manager = JobManager(app)
    args = None
    schedule_task = ScheduleMonitorsTask.from_args(args, manager)
    schedule_task.run()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/v1/api/*": {"origins": "*"}})

    app_settings = os.getenv(
        'APP_SETTINGS',
        'monosi.server.config.Config'
    )
    app.config.from_object(app_settings)
    
    load_monitors(app)

    return app

