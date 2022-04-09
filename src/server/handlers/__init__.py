from .datasources import (
    DataSourceListResource,
    DataSourceTestResource,
    DataSourceResource,
)
from .integrations import (
    IntegrationListResource,
    IntegrationResource,
)
from .issues import (
    IssueListResource,
)
from .metrics import (
    MetricListResource,
)
from .monitors import (
    MonitorListResource,
    MonitorResource,
)

def init_api(api):
    api.add_resource(IntegrationListResource, '/{}/integrations'.format(api.PREFIX))
    api.add_resource(IntegrationResource, '/{}/integrations/<int:obj_id>'.format(api.PREFIX))

    api.add_resource(IssueListResource, '/{}/issues'.format(api.PREFIX))

    api.add_resource(DataSourceListResource, '/{}/datasources'.format(api.PREFIX))
    api.add_resource(DataSourceResource, '/{}/datasources/<int:obj_id>'.format(api.PREFIX))
    api.add_resource(DataSourceTestResource, '/{}/datasources/<int:obj_id>/test'.format(api.PREFIX))
    
    api.add_resource(MonitorListResource, '/{}/monitors'.format(api.PREFIX))
    api.add_resource(MonitorResource, '/{}/monitors/<int:obj_id>'.format(api.PREFIX))

    api.add_resource(MetricListResource, '/{}/monitors/<int:monitor_id>/metrics'.format(api.PREFIX))

