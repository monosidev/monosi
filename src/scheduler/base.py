from datetime import datetime, timedelta
from flask_apscheduler import APScheduler
import json
import uuid
import logging

# from monosi.scheduler.db import db
import scheduler.constants as constants
from .models.execution import Execution

logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def import_from_path(path):
    components = path.split('.')
    module = __import__('.'.join(components[:-1]))
    for comp in components[1:-1]:
        module = getattr(module, comp)
    return getattr(module, components[-1])

class MsiScheduler(APScheduler):
    @classmethod
    def run_job(cls, func, job_id, *args, **kwargs):
        execution = Execution(
            job_id=job_id,
            state=constants.STATUS_SCHEDULED
        )
        execution.create()
        execution_id = execution.id

        try:
            execution.update(updates={"state": constants.STATUS_SCHEDULED})

            cls.run_scheduler_job(func, execution_id, *args, **kwargs)
        except Exception:
            execution.update(updates={"state": constants.STATUS_SCHEDULED_ERROR})

            return None
        return execution_id

    @classmethod
    def run_scheduler_job(cls, func, execution_id, *args, **kwargs):
        try:
            execution = Execution.get_by_id(execution_id)
            execution.update(updates={"state": constants.STATUS_RUNNING})

            result = func()
            result_json = json.dumps(result, indent=4, sort_keys=True)

            execution.update(updates={
                "state": constants.STATUS_SUCCEEDED,
                "result": result_json
            })

        except Exception as err:
            print("Error: {0}".format(err))
            if execution:
                execution.update({
                    "state": constants.STATUS_FAILED
                })


    def add_scheduler_job(self, monitor_job, job_id=None, args=None, trigger='interval', minutes=720, **kwargs):
        if not job_id:
            job_id = str(uuid.uuid4().hex)

        minutes = int(minutes)

        execution = Execution.get_by_job_id(job_id)
        if execution:
            monitor_job.task.monitor.minutes_ago = int((datetime.now() - execution.created_at).seconds / 60)

        if not args:
            args = []
        arguments = [monitor_job.run, job_id]
        arguments.extend(args)

        start_date = datetime.now() - timedelta(minutes=(minutes-1)) # start one minute after schedule

        self.add_job(func=self.run_job, id=job_id, args=arguments, trigger=trigger, minutes=minutes, start_date=start_date)

        return job_id
