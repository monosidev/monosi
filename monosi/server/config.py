import os
basedir = os.path.abspath(os.path.dirname(__file__))

monosi_path = os.path.expanduser("~/.monosi")
if not os.path.exists(monosi_path):
    os.makedirs(monosi_path)

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + monosi_path + "/sqlite.db"

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False

Config = DevelopmentConfig
if os.getenv('FLASK_ENV') == "production":
    Config = ProductionConfig
