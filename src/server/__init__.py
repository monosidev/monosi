from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import sys
import uuid

from core.common.events import set_user_id

from .api import MsiApi
from .db import db
from .models.monitor import Monitor
from .models.integration import Integration
from .scheduler import manager

curr_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(curr_path, "../"))
sys.path.append(src_path)

def _build_path():
    build_path = os.path.join(src_path, 'ui/build/')
    if not os.path.exists(build_path):
        raise Exception("Client UI was not built before attempting to serve via Flask.")

    return build_path

def _serve_ui(path=''):
    build_path = _build_path()
    req_path = os.path.join(build_path, path)

    if req_path == build_path or not os.path.exists(req_path):
        path = "index.html"

    return send_from_directory(build_path, path)

def _init_ui(app):
    if not app.config['SERVE_UI']:
        return

    app.static_folder =  os.path.join(_build_path(), "static")
    app.add_url_rule("/", view_func=_serve_ui)
    app.add_url_rule("/<path:path>", view_func=_serve_ui)


def create_app():
    # Initialize Server
    app = Flask(__name__)
    CORS(app, resources={r"/v1/api/*": {"origins": "*"}})
    app_settings = os.getenv(
        'APP_SETTINGS',
        'server.config.Config'
    )
    app.config.from_object(app_settings)

    # Initialize UI if SERVE_UI
    _init_ui(app)

    # Initialize DB
    db.init_app(app)
    db.app = app
    with app.app_context():
        db.create_all()

    # Initialize API
    api = MsiApi(app)

    # Initialize monitor jobs
    manager.init_app(app)
    with app.app_context():
        [monitor.schedule() for monitor in Monitor.all()]

    [integration.register() for integration in Integration.all()]

    set_user_id(str(uuid.uuid4()))

    return app
