import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from core.drivers.postgres import DriverConfiguration

def monosi_home_dir():
    monosi_path = os.path.expanduser("~/.monosi")
    if not os.path.exists(monosi_path):
        os.makedirs(monosi_path)

    return monosi_path

db_config = DriverConfiguration(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_DATABASE'),
    schema=os.getenv('DB_SCHEMA'),
    port=os.getenv('DB_PORT'),
)

class BaseConfig:
    """Base configuration."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    SERVE_UI = bool(os.getenv('SERVE_UI', False))
    SQLALCHEMY_DATABASE_URI = db_config.connection_string()
    SCHEDULER_JOBSTORES = {"default": SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI, tablename="msi_jobs")}
    SCHEDULER_API_ENABLED = True

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True

class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False

Config = DevelopmentConfig
if os.getenv('FLASK_ENV') == "production":
    Config = ProductionConfig
