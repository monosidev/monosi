from core.common.events import track_event

from . import create_app

track_event(None, action="server_start", label="")
app = create_app()

