from flask_apscheduler import APScheduler
import json
import uuid
import logging

from monosi.scheduler.db import db
from monosi.scheduler.models.execution import Execution
import monosi.scheduler.constants as constants

logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def import_from_path(path):
    components = path.split('.')
    module = __import__('.'.join(components[:-1]))
    for comp in components[1:-1]:
        module = getattr(module, comp)
    return getattr(module, components[-1])

class MonosiScheduler(APScheduler):
    @classmethod
    def run_job(cls, job_class_str, job_id, *args, **kwargs):
        execution = Execution(
            job_id=job_id,
            state=constants.EXECUTION_STATUS_SCHEDULED
        )
        execution.create()
        execution_id = execution.id

        try:
            job_class = import_from_path(job_class_str)
            execution.update(updates={"state": constants.EXECUTION_STATUS_SCHEDULED})

            cls.run_scheduler_job(job_class, execution_id, *args, **kwargs)
        except Exception:
            execution.update(updates={"state": constants.EXECUTION_STATUS_SCHEDULED_ERROR})

            return None
        return execution_id

    @classmethod
    def run_scheduler_job(cls, job_class, execution_id, *args, **kwargs):
        try:
            execution = Execution.get_by_id(execution_id)
            execution.update(updates={"state": constants.EXECUTION_STATUS_RUNNING})

            result = job_class.run()
            result_json = json.dumps(result, indent=4, sort_keys=True)

            execution.update(updates={
                "state": constants.EXECUTION_STATUS_SUCCEEDED,
                "result": result_json
            })

        except Exception as err:
            print("Error: {0}".format(err))
            if execution:
                execution.update({
                    "state": constants.EXECUTION_STATUS_FAILED
                })

    def add_scheduler_job(self, job_class_str, args=None, trigger='interval', minutes=720, **kwargs):
        job_id = uuid.uuid4().hex

        if not args:
            args = []
        arguments = [job_class_str, job_id]
        arguments.extend(args)

        self.add_job(func=self.run_job, id=job_id, args=arguments, trigger=trigger, minutes=minutes)

        return job_id
