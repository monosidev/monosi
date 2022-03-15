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