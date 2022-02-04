from scheduler.db import db

class Execution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=db.func.now(), onupdate=db.func.now())

    __tablename__ = "executions"

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter(cls.id == _id).order_by(cls.created_at).one()

    @classmethod
    def get_by_job_id(cls, _id):
        return cls.query.filter(cls.job_id == _id).order_by(cls.created_at).first()

    @classmethod
    def delete_by_job_id(cls, _id):
        db.session.delete(cls.query.filter(cls.job_id == _id))
        db.session.commit()
        
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    def update(self, updates):
        for k, v in updates.items():
            setattr(self, k, v)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls):
        return cls.query.all()
