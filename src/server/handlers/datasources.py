from core.models.datasource import DataSource

from .base import CrudResource, ListResource

class DataSourceResource(CrudResource):
    @property
    def resource(self):
        return DataSource

    @property
    def key(self):
        return "datasources"

class DataSourceListResource(ListResource):
    @property
    def resource(self):
        return DataSource

    @property
    def key(self):
        return "datasources"