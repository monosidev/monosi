from flask import Flask
from flask_cors import CORS
import os

from .api import init_api
from .db import init_db
from .scheduler import init_scheduler
from .ui import init_ui

middleware = [
    init_api,
    init_db,
    init_scheduler,
    init_ui,
]


def create_app():
    # Initialize Server
    app = Flask(__name__)
    CORS(app, resources={r"/v1/api/*": {"origins": "*"}})
    app_settings = os.getenv(
        'APP_SETTINGS',
        'server.config.Config'
    )
    app.config.from_object(app_settings)

    # Middleware
    [func(app) for func in middleware]

    return app
