from datetime import datetime, timedelta
from flask_apscheduler import APScheduler
from sqlalchemy.orm import sessionmaker
import json
import uuid
import logging

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

# from monosi.scheduler.db import db
import scheduler.constants as constants
from .models.execution import Execution
from .models import mapper_registry

logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def import_from_path(path):
    components = path.split('.')
    module = __import__('.'.join(components[:-1]))
    for comp in components[1:-1]:
        module = getattr(module, comp)
    return getattr(module, components[-1])

class MsiJobStore(SQLAlchemyJobStore):
    def __init__(self, url):
        super().__init__(url=url, tablename='msi_jobs')
        mapper_registry.metadata.create_all(self.engine)

    def create(self, obj):
        execution_id = None

        Session = sessionmaker(self.engine)
        with Session() as session:
            execution = Execution.from_dict(obj)
            session.add(execution)
            session.commit()

            execution_id = execution.id
            session.expunge_all()
        
        return execution_id

    def update(self, obj):
        Session = sessionmaker(self.engine)
        with Session() as session:
            session.query(Execution).filter(Execution.id == obj['id']).update({
                'state': obj['state'],
                'result': obj.get('result'),
            }, synchronize_session = False)
            session.commit()
            session.expunge_all()

    def get(self, id):
        execution = {}
        try:
            Session = sessionmaker(self.engine)
            with Session() as session:
                obj = session.query(Execution).filter(Execution.datasource_id == id).order_by(Execution.created_at).first()
                if obj is not None:
                    execution = obj.to_dict()

                session.expunge_all()
        except Exception as e:
            logging.warn(e)
            logging.warn("No execution found for datasource id: {}", id)

        return execution


class MsiScheduler(APScheduler):
    def __init__(self, db_url, *args, **kwargs):
        self.db_url = db_url
        super().__init__(*args, **kwargs)
        self.api_prefix = '/v1/api'

    def jobstore(self):
        return MsiJobStore(self.db_url)

    @classmethod
    def run_job(cls, job_class_path, job_id, db_url, *args, **kwargs):
        datasource_id = args[0]

        jobstore = MsiJobStore(url=db_url)
        last_run = jobstore.get(datasource_id).get('updated_at')

        execution_id = jobstore.create({
            'job_id': job_id,
            'state': constants.STATUS_SCHEDULED,
            'result': None,
            'datasource_id': datasource_id,
        })

        try:
            job_class = import_from_path(job_class_path)
            jobstore.update({
                'id': execution_id,
                'state': constants.STATUS_SCHEDULED,
            })

            cls.run_scheduler_job(job_class, job_id, execution_id, jobstore, last_run, *args, **kwargs)
        except Exception as e:
            logging.error(e)
            jobstore.update({
                'id': execution_id,
                'state': constants.STATUS_SCHEDULED_ERROR,
            })
            return None

        return execution_id

    @classmethod
    def run_scheduler_job(cls, job_class, job_id, execution_id, jobstore, last_run, *args, **kwargs):
        try:
            jobstore.update({
                'id': execution_id,
                'state': constants.STATUS_RUNNING,
            })

            result = job_class.run_job(job_id, last_run, execution_id, *args, **kwargs)
            jobstore.update({
                'id': execution_id,
                'state': constants.STATUS_SUCCEEDED,
                'updated_at': datetime.now(),
            })
        except Exception as err:
            jobstore.update({
                'id': execution_id,
                'state': constants.STATUS_FAILED,
                'result': repr(err),
                'updated_at': datetime.now(),
            })
            logging.error("Error: {0}".format(err))

    def add_scheduler_job(self, job_class_string, name, job_id=None, job_args=None, trigger='interval', minutes=720, **kwargs):
        if not job_args:
            job_args = []

        if not job_id:
            job_id = uuid.uuid4().hex

        args = [job_class_string, job_id, self.db_url]
        args.extend(job_args)

        start_date = datetime.now() - timedelta(minutes=(minutes-1)) # start one minute after schedule
        self.add_job(func=self.run_job, id=job_id, args=args, trigger=trigger, minutes=minutes, start_date=start_date, name=name, **kwargs)

        return job_id

    def _load_api(self):
        """
        Add the routes for the scheduler API.
        """
        from flask_apscheduler import api
        self._add_url_route('get_job', '/jobs/<job_id>', api.get_job, 'GET')
        self._add_url_route('get_jobs', '/jobs', api.get_jobs, 'GET')

