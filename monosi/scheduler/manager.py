from monosi.scheduler.base import MonosiScheduler
from monosi.scheduler.db import db

class JobManager:
    singleton = None

    def __init__(self, app=None):
        if JobManager.singleton is None:
            self.app = app
            self.scheduler = MonosiScheduler()
            if app is not None:
                self.init_app(app)
            JobManager.singleton = self

    def init_app(self, app):
        self.scheduler.init_app(app)

        db.init_app(app)
        with app.app_context():
            db.create_all()

        self.start()

    def start(self):
        return self.scheduler.start()

    def stop(self):
        return self.scheduler.shutdown()

    def add_job(self, job, args=None, trigger='interval', minutes=720, **kwargs):
        return self.scheduler.add_scheduler_job(job, args=args, trigger=trigger, minutes=minutes)

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

