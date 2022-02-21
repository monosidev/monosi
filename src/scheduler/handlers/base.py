from flask_restful import Resource

class BaseResource(Resource):
    def app_db(self):
        from scheduler.manager import JobManager
        return JobManager.jobstore().engine
