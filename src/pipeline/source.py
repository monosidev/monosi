import json
import logging
from sqlalchemy.orm import sessionmaker, Session
from typing import List
from ingestion.sources.postgresql import PostgreSQLSourceConfiguration

from ingestion.sources import PostgreSQLSource, SQLAlchemyExtractor
from ingestion.task import TaskUnit

class MsiInternalSourceExtractor(SQLAlchemyExtractor):
    def __init__(self, configuration):
        self.configuration = configuration
        self.engine = None
        self.connection = None

    def _initialize(self):
        if self.engine and self.connection:
            return

        self.engine = self._create_engine()
        self.connection = self.engine.connect()

    def _execute(self, model):
        objs = []
        try:
            Session = sessionmaker(self.engine)
            with Session() as session:
                objs = session.query(model).all()
        except Exception as e:
            logging.error("Couldn't retrieve metrics: {}", e)

        return objs
    
    def run(self, unit: TaskUnit):
        self._initialize()

        model = unit.request()
        results = self._execute(model)

        return results

class MsiInternalSourceConfiguration(PostgreSQLSourceConfiguration):
    @property
    def type(self):
        return "msi_internal"

class MsiInternalSource(PostgreSQLSource):
    def __init__(self, configuration: MsiInternalSourceConfiguration):
        super().__init__(configuration)

    def _metrics(self):
        from server.models import Metric
        return Metric

    def task_units(self) -> List[TaskUnit]:
        return [
            TaskUnit(request=self._metrics)
        ]

    def extractor(self):
        return MsiInternalSourceExtractor(self.configuration)

