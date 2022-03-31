import json

from ingestion.sources.base import SQLAlchemyExtractor

from .postgresql import PostgreSQLSource, PostgreSQLSourceConfiguration

class RedshiftSourceConfiguration(PostgreSQLSourceConfiguration):
    def _connection_string_prefix(self) -> str:
        return "redshift+psycopg2"

    @property
    def type(self):
        return "redshift"

class RedshiftExtractor(SQLAlchemyExtractor):
    def _initialize(self):
        super()._initialize()
        self._execute("SET enable_case_sensitive_identifier TO true;")

class RedshiftSource(PostgreSQLSource):
    def extractor(self):
        return RedshiftExtractor(self.configuration)

