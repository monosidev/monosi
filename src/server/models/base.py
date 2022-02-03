# from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_base, registry
from server.db import db

# class BaseModel(Base):
#     query_class = MsiQuery

class CrudMixin(object):
    # id = Column(Integer, primary_key=True)
    # updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    # created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())

    # @classmethod
    # def validate(cls, model_dict):
    #     pass

    # @classmethod
    # def from_dict(cls, model_dict):
    #     pass

    # def to_dict(self):
    #     pass

    @classmethod
    def all(cls):
        try:
            return cls.query.all()
        except Exception as e:
            raise Exception("DB: Couldn't query all records")

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            raise Exception("DB: Couldn't persist record")

    def update(self, updates):
        try:
            for k, v in updates.items():
                setattr(self, k, v)
            db.session.commit()
        except Exception as e:
            raise Exception("DB: Couldn't update record")

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            raise Exception("DB: Couldn't delete record")
