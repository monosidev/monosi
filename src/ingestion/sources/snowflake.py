import json

from .base import SourceConfiguration, SQLAlchemySourceDialect, SQLAlchemySource

class SnowflakeSourceConfiguration(SourceConfiguration):
	@classmethod
	def validate(cls, configuration):
        return {
            "type": "object",
            "properties": {
                "user": { "type": "string" },
                "password": { "type": "string" },
                "account": { "type": "string" },
                "database": { "type": "string" },
                "warehouse": { "type": "string" },
                "schema": { "type": "string" },
            },
            "secret": [ "password" ],
        }

    def connection_string(self) -> str:
    	configuration = json.loads(self.configuration)

        return 'snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}'.format(
            user=configuration.get('user'),
            password=configuration.get('password'),
            account=configuration.get('account'),
            database=configuration.get('database'),
            warehouse=configuration.get('warehouse'),
            schema=configuration.get('schema'),
        )

    @property
	def type(self):
		return "snowflake"

class SnowflakeSourceDialect(SQLAlchemySourceDialect):
    @classmethod
    def _text_int_rate(cls):
        return "SUM(IFF(REGEXP_COUNT(TO_VARCHAR({}), '^([-+]?[0-9]+)$', 1, 'i') != 0, 1, 0)) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _text_number_rate(cls):
        return "SUM(IFF(REGEXP_COUNT(TO_VARCHAR({}), '^([-+]?[0-9]*[.]?[0-9]+([eE][-+]?[0-9]+)?)$', 1, 'i') != 0, 1, 0)) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _text_uuid_rate(cls):
        return "SUM(IFF(REGEXP_COUNT(TO_VARCHAR({}), '^([0-9a-fA-F]{{8}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{12}})$', 1, 'i') != 0, 1, 0)) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _text_all_spaces_rate(cls):
        return "SUM(IFF(REGEXP_COUNT(TO_VARCHAR({}), '^(\\\\s+)$', 1, 'i') != 0, 1, 0)) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _text_null_keyword_rate(cls):
        return "SUM(IFF(UPPER({}) IN ('NULL', 'NONE', 'NIL', 'NOTHING'), 1, 0)) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _zero_rate(cls):
        return "SUM(IFF(UPPER({}) IN ('NULL', 'NONE', 'NIL', 'NOTHING'), 1, 0)) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _negative_rate(cls):
        return "SUM(IFF({} < 0, 1, 0)) / CAST(COUNT(*) AS NUMERIC)"

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


class SnowflakeSource(SQLAlchemySource):
	dialect: SnowflakeSourceDialect

