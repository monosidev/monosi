from .datasources import (
    DataSourceListResource,
    DataSourceResource,
)
from .integrations import (
    IntegrationListResource,
    IntegrationResource,
)
from .metrics import (
	MetricListResource,
	MetricResource,
)
from .monitors import (
    MonitorListResource,
    MonitorResource,
    RunMonitorResource,
)

def init_api(api):
	api.add_resource(IntegrationListResource, '/{}/integrations'.format(api.PREFIX))
	api.add_resource(IntegrationResource, '/{}/integrations/<int:obj_id>'.format(api.PREFIX))

	api.add_resource(DataSourceListResource, '/{}/datasources'.format(api.PREFIX))
	api.add_resource(DataSourceResource, '/{}/datasources/<int:obj_id>'.format(api.PREFIX))

	api.add_resource(MonitorListResource, '/{}/monitors'.format(api.PREFIX))
	api.add_resource(MonitorResource, '/{}/monitors/<int:obj_id>'.format(api.PREFIX))
	api.add_resource(RunMonitorResource, '/{}/monitors/<int:obj_id>/run'.format(api.PREFIX))

	api.add_resource(MetricListResource, '/{}/monitors/<int:obj_id>/metrics'.format(api.PREFIX))
	api.add_resource(MetricResource, '/{}/monitors/<int:obj_id>/metrics/<string:metric_name>'.format(api.PREFIX))
