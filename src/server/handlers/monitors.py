from server.models.monitor import Monitor
from .base import CrudResource, ListResource

class MonitorListResource(ListResource):
    @property
    def resource(self):
        return Monitor

    @property
    def key(self):
        return "monitors"

class MonitorResource(CrudResource):
    @property
    def resource(self):
        return Monitor

    @property
    def key(self):
        return "monitor"
