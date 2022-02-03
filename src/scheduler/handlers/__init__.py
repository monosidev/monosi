from flask_restful import Api

from .executions import ExecutionsListResource, ExecutionsResource

def init_api(api):
    # TODO: Provide monitor_id/job_id spaced retrieval
    api.add_resource(ExecutionsListResource, '/v1/api/executions')
    api.add_resource(ExecutionsResource, '/v1/api/execution/<execution_id>')
