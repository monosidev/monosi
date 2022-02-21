from .executions import ExecutionsListResource, ExecutionsResource
# from .jobs import JobListResource, JobResource
# from .logs import LogListResources


def init_api(api):
    api.add_resource(ExecutionsListResource, '/{}/executions'.format(api.PREFIX))
    api.add_resource(ExecutionsResource, '/{}/executions/<int:obj_id>'.format(api.PREFIX))

    # api.add_resource(JobListResource, '/{}/jobs'.format(api.PREFIX))
    # api.add_resource(JobResource, '/{}/jobs/<int:obj_id>'.format(api.PREFIX))

    # api.add_resource(LogListResource, '/{}/logs'.format(api.PREFIX))
