from scheduler.manager import JobManager

from server.config import Config


# Initialize scheduler process
manager = JobManager(db_url=Config.SQLALCHEMY_DATABASE_URI)

def init_scheduler(app):
    manager.init_app(app)
    return manager    

