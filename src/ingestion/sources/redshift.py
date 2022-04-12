import json

from ingestion.sources.base import SQLAlchemyExtractor

from .postgresql import PostgreSQLSource, PostgreSQLSourceConfiguration, PostgreSQLSourceDialect

class RedshiftSourceConfiguration(PostgreSQLSourceConfiguration):
    def _connection_string_prefix(self) -> str:
        return "redshift+psycopg2"

    @property
    def type(self):
        return "redshift"

class RedshiftSourceDialect(PostgreSQLSourceDialect):
    @classmethod
    def _freshness(cls):
        return "DATEDIFF(MINUTE, MAX(CAST({} AS TIMESTAMP)), GETDATE())"


class RedshiftExtractor(SQLAlchemyExtractor):
    def _initialize(self):
        super()._initialize()
        self._custom_execute("SET enable_case_sensitive_identifier TO true;")

    # TODO: This is a hacky solution, need to update _execute method in base to support non SELECT statements
    def _custom_execute(self, sql: str):
        if not self.connection:
            raise Exception("Connection has already been closed. Could not execute.")
        
        self.connection.execute(sql)

class RedshiftSource(PostgreSQLSource):
    def __init__(self, configuration: RedshiftSourceConfiguration):
        self.configuration = configuration
        self.dialect = RedshiftSourceDialect
        
    def extractor(self):
        return RedshiftExtractor(self.configuration)

