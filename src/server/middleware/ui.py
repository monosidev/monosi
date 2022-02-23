import os
import sys

from flask import send_from_directory

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

def init_ui(app):
    if not app.config['SERVE_UI']:
        return

    app.static_folder =  os.path.join(_build_path(), "static")
    app.add_url_rule("/", view_func=_serve_ui)
    app.add_url_rule("/<path:path>", view_func=_serve_ui)
