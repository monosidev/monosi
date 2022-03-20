from flask_restful import abort
from sqlalchemy.orm import sessionmaker

from scheduler import constants
from scheduler.models.execution import Execution

from .base import BaseResource
        
def _state_to_str(execution_dict):
    prev_state = execution_dict['state']
    execution_dict['state'] = constants.STATUS_DICT[prev_state]
    return execution_dict

class ExecutionsListResource(BaseResource):
    def get(self):
        Session = sessionmaker(self.app_db())
        with Session() as session:
            executions = session.query(Execution).all()
            executions_dict_list = [_state_to_str(execution.to_dict()) for execution in executions]

        return {"executions": executions_dict_list}


    # TODO: Execute on demand

class ExecutionsResource(BaseResource):
    def _retrieve_by_id(self, execution_id):
        try:
            Session = sessionmaker(self.app_db())
            with Session() as session:
                executions = session.query(Execution).filter(Execution.datasource_id == execution_id).all()
        except:
            abort(404)
        return executions

    def get(self, obj_id):
        executions = self._retrieve_by_id(obj_id) # This is actually datasource_id

        return {"executions": [_state_to_str(execution.to_dict()) for execution in executions]}
