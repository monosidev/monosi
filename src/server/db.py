from flask_sqlalchemy import BaseQuery, SQLAlchemy

from .models import Base

class MsiQuery(BaseQuery):
    def get_by_id(cls, ident, default=None):
        return self.get(ident) or default

    # def all(cls):
    #     return cls.query.all()
    
    # def create(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def update(self, updates):
    #     for k, v in updates.items():
    #         setattr(self, k, v)
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()

db = SQLAlchemy(model_class=Base, query_class=MsiQuery)

