import logging

from .api import init_api
from .base import MsiScheduler

class JobManager:
    singleton = None

    def __init__(self, app=None, db_url=None):
        self.app = app
        self.scheduler = MsiScheduler(db_url=db_url)

        if app is not None:
            self.init_app(app)

        JobManager.singleton = self

    def init_app(self, app):
        # Initialize scheduler
        self.scheduler.init_app(app)
        self.scheduler.app = app

        # Initialize API
        init_api(app)

        try:
            self.start()
            logging.info("The scheduler started successfully.")
        except Exception as e:
            logging.warn("The scheduler failed to start.")
            raise e

    @classmethod
    def jobstore(cls):
        if cls.singleton is None:
            return

        return cls.singleton.scheduler.jobstore()

    def start(self):
        return self.scheduler.start()

    def stop(self):
        return self.scheduler.shutdown()

    def add_job(self, job_class_string, name=None, args=None, trigger='interval', minutes=120, job_id=None, **kwargs):
        return self.scheduler.add_scheduler_job(job_class_string, job_id=job_id, name=name, job_args=args, trigger=trigger, minutes=minutes, **kwargs)

    def pause_job(self, job_id):
        return self.scheduler.pause_job(job_id)

    def get_job(self, job_id):
        return self.scheduler.get_job(job_id)

    def get_jobs(self):
        return self.scheduler.get_jobs()

    def remove_job(self, job_id):
        return self.scheduler.remove_job(job_id)

    def resume_job(self, job_id):
        return self.scheduler.resume_job(job_id)

    def add_listener(self, listener, events):
        return self.scheduler.add_listener(listener, events)

    def remove_listener(self, listener):
        return self.scheduler.remove_listener(listener)

