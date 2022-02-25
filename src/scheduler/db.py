from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import mapper_registry

class SchedulerDatabase:
    def __init__(self, url):
        self.engine = self._create_engine(url)

    def _create_engine(self, url):
        try:
            engine = create_engine(url)
            mapper_registry.metadata.create_all(engine)

            return engine
        except Exception as e:
            raise e

    def add(self, obj):
        Session = sessionmaker(self.engine)
        with Session() as session:
            session.add(obj)
            session.commit()

