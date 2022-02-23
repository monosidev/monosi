import logging
from core.events import track_event
from core.models.datasource import DataSource

from .base import CrudResource, ListResource

class DataSourceResource(CrudResource):
    @property
    def resource(self):
        return DataSource

    @property
    def key(self):
        return "datasource"

class DataSourceListResource(ListResource):
    @property
    def resource(self):
        return DataSource

    @property
    def key(self):
        return "datasources"

    def _after_create(self, sqlalc_obj):
        track_event(action="connection_created", label=sqlalc_obj.type)

class DataSourceTestResource(CrudResource):
    @property
    def resource(self):
        return DataSource

    @property
    def key(self):
        return "datasource"

    def _test(self, obj):
        driver = obj.db_driver()
        return driver.test()

    def get(self, **kwargs):
        obj_id = kwargs['obj_id']
        obj = self._retrieve_by_id(obj_id)

        result = self._test(obj)
        return {self.key: {"connection": result}}
