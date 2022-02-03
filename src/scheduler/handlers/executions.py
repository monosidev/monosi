import abc
import logging
from flask import request
from flask_restful import Resource, abort

from scheduler.models.execution import Execution


class ExecutionsListResource(Resource):
    def get(self):
        executions = Execution.all()
        executions_dict_list = [execution.to_dict() for execution in executions]

        return {"executions": executions_dict_list}

    # TODO: Execute on demand

class ExecutionsResource(Resource):
    def _retrieve_by_id(self, execution_id):
        try:
            execution = Execution.query.get(execution_id)
        except:
            abort(404)
        return execution

    def get(self, execution_id):
        execution = self._retrieve_by_id(execution_id)

        return {"execution": execution.to_dict()}
