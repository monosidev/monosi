import os

def monosi_home_dir():
    monosi_path = os.path.expanduser("~/.monosi")
    if not os.path.exists(monosi_path):
        os.makedirs(monosi_path)

    return monosi_path

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + monosi_home_dir() + "/sqlite.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVE_UI = bool(os.getenv('SERVE_UI', False))

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
