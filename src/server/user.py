from dataclasses import dataclass
import uuid

from server.middleware.db import db


class User(db.Model):
    id = db.Column(db.String(50), primary_key=True, nullable=False)

    __tablename__ = "msi_users"

    @classmethod
    def create_or_load(cls):
        def extract_count(num_users):
            try:
                return num_users[0][0]
            except:
                return 0

        num_users = db.session.query(db.func.count(cls.id)).all()
        if extract_count(num_users) == 0:
            db.session.add(User(id=uuid.uuid4().hex))
            db.session.commit()

        return db.session.query(cls).one().id
