from .datasources import (
	DatasourceListResource,
	DatasourceResource,
)
from .integrations import (
    IntegrationListResource,
    IntegrationResource,
)
from .monitors import (
    MonitorListResource,
    MonitorResource,
)

def init_api(api):
	api.add_resource(DatasourceListResource, '/v1/api/datasources')
	api.add_resource(DatasourceResource, '/v1/api/datasources/<obj_id>')

	api.add_resource(IntegrationListResource, '/v1/api/integrations')
	api.add_resource(IntegrationResource, '/v1/api/integrations/<obj_id>')

	api.add_resource(MonitorListResource, '/{}/monitors'.format(api.PREFIX))
	api.add_resource(MonitorResource, '/{}/monitors/<obj_id>'.format(api.PREFIX))
