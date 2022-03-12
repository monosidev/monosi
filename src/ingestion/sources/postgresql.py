import json

from .base import SourceConfiguration, SQLAlchemySourceDialect, SQLAlchemySource

class PostgreSQLSourceConfiguration(SourceConfiguration):
	@classmethod
	def validate(cls, configuration):
        return {
            "type": "object",
            "properties": {
                "user": { "type": "string" },
                "password": { "type": "string" },
                "host": { "type": "string" },
                "port": { "type": "string" },
                "database": { "type": "string" },
                "schema": { "type": "string" },
            },
            "secret": [ "password" ],
        }

    def connection_string(self) -> str:
        configuration = json.loads(self.configuration)

        return 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
            user=configuration.get('user'),
            password=configuration.get('password'),
            host=configuration.get('host'),
            port=configuration.get('port'),
            database=configuration.get('database'),
            schema=configuration.get('schema'),
        )

    @property
	def type(self):
		return "postgresql"

class PostgreSQLSourceDialect(SQLAlchemySourceDialect):
    @classmethod
    def _numeric_std(cls):
        return "STDDEV(CAST({} as double precision))"
    
    @classmethod
    def _text_int_rate(cls):
        return "SUM(CASE WHEN CAST({} AS varchar) ~ '^([-+]?[0-9]+)$' THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _text_number_rate(cls):
        return "SUM(CASE WHEN CAST({} AS varchar) ~ '^([-+]?[0-9]*[.]?[0-9]+([eE][-+]?[0-9]+)?)$' THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _text_uuid_rate(cls):
        return "SUM(CASE WHEN CAST({} AS varchar) ~ '^([0-9a-fA-F]{{8}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{12}})$' THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _text_all_spaces_rate(cls):
        return "SUM(CASE WHEN CAST({} AS varchar) ~ '^(\\\\s+)$' THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _text_null_keyword_rate(cls):
        return "SUM(CASE WHEN UPPER(CAST({} as varchar)) IN ('NULL', 'NONE', 'NIL', 'NOTHING') THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _zero_rate(cls): # TODO: ?
        return "SUM(CASE WHEN UPPER(CAST({} as varchar)) IN ('NULL', 'NONE', 'NIL', 'NOTHING') THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _negative_rate(cls):
        return "SUM(CASE WHEN {} < 0 THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _completeness(cls):
        return "COUNT({}) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def schema_query(cls):
    	raise NotImplementedError

    @classmethod
    def table_metrics_query(cls):
    	raise NotImplementedError

    @classmethod
    def query_access_logs_query(cls):
    	raise NotImplementedError
    	
    @classmethod
    def query_copy_logs_query(cls):
    	raise NotImplementedError


class PostgreSQLSource(SQLAlchemySource):
	dialect: PostgreSQLSourceDialect
