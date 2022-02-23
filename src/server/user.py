from dataclasses import dataclass
import uuid

from .middleware.db import db

class User(db.Model):
    id = db.Column(db.String(50))

    @classmethod
    def create_or_load(cls):
        num_users = db.query(db.func.count(cls)).all()
        if num_users == 0:
            db.session.add(User(id=uuid.uuid4().hex))
            db.session.commit()

        return db.query(cls).one().id



