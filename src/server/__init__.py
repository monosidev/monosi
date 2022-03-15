from flask import Flask
from flask_cors import CORS
import os
import sys

curr_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(curr_path, "../"))
sys.path.append(src_path)

from server.middleware import middleware
from server.user import User
from telemetry.events import set_user_id, track_event


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

    set_user_id(User.create_or_load())
    track_event(action="server_start")

    return app
