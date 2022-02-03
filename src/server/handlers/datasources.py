from server.models.datasource import Datasource
from .base import CrudResource, ListResource

class DatasourceListResource(ListResource):
    @property
    def resource(self):
        return Datasource

    @property
    def key(self):
        return "datasources"

class DatasourceResource(CrudResource):
    @property
    def resource(self):
        return Datasource

    @property
    def key(self):
        return "datasource"

