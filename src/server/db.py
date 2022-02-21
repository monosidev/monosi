from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base

from core.models import mapper_registry

Base = declarative_base(metadata=mapper_registry.metadata)
db = SQLAlchemy(model_class=Base)

def init_db(app):
    db.init_app(app)
    db.app = app

    with app.app_context():
        db.create_all()
    
    return db
