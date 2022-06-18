import json
from typing import Any
from urllib.parse import quote

from ingestion.task import TaskUnit

from .base import (
    MetricsQueryBuilder,
    SourceConfiguration,
    SQLAlchemySourceDialect,
    SQLAlchemySource,
    SQLAlchemyExtractor
)

class MSSQLMetricsQueryBuilder(MetricsQueryBuilder):
    def _base_query_backfill(self, select_sql, table, timestamp_field): # TODO
        return """
            SELECT 
                DATEPART(HOUR, {timestamp_field}) as "WINDOW_START", 
                DATEPART(HOUR, {timestamp_field}) + interval '1 hour' as "WINDOW_END",
                COUNT(*) as "ROW_COUNT",
                '{table}' as "TABLE_NAME",
                '{database}' as "DATABASE_NAME",
                '{schema}' as "SCHEMA_NAME",

                {select_sql}
            FROM {table} as c
            WHERE 
                DATEPART(HOUR, {timestamp_field}) >= CURRENT_TIMESTAMP + interval '{minutes_ago} minutes' 
            GROUP BY "WINDOW_START", "WINDOW_END" 
            ORDER BY "WINDOW_START" ASC;
        """.format(
            select_sql=select_sql,
            table=table,
            timestamp_field=timestamp_field,
            minutes_ago=self.minutes_ago,
            database=self.monitor['database'],
            schema=self.monitor['schema'],
        )

class MSSQLSourceConfiguration(SourceConfiguration):
    @classmethod
    def validate(cls, configuration):
        raise NotImplementedError

    @classmethod
    def configuration_schema(cls):
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
    
    def _connection_string_prefix(self):
        return "mssql+pyodbc"

    def connection_string(self) -> str:
        configuration = json.loads(self.configuration)
        connection_string_prefix = self._connection_string_prefix()

        return '{prefix}://{user}:{password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server")'.format(
            prefix=connection_string_prefix,
            user=configuration.get('user'),
            password=configuration.get('password'),
            host=configuration.get('host'),
            port=configuration.get('port'),
            database=configuration.get('database'),
            schema=configuration.get('schema'),
        )

    @property
    def type(self):
        return "mssql"

class MSSQLSourceDialect(SQLAlchemySourceDialect):
    @classmethod
    def _freshness(cls):
        return "(DATEPART(day, CURRENT_TIMESTAMP - MAX({0})) * 24 + DATEPART(hour, CURRENT_TIMESTAMP - MAX({0}))) * 60 + DATEPART(minute, CURRENT_TIMESTAMP - MAX({0}))"

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
    def schema_tables_query(cls, database_name, schema_name):
        raise NotImplementedError

    @classmethod
    def table_metrics_query(cls, monitor, discovery_data, minutes_ago):
        builder = MSSQLMetricsQueryBuilder(cls, monitor, discovery_data, minutes_ago)
        query = builder.compile()
        return query

    @classmethod
    def schema_columns_query(cls, database_name, schema_name):
        return """
        SELECT lower(c.table_name) AS "NAME",
            lower(c.column_name) AS "COL_NAME",
            lower(c.data_type) AS "COL_TYPE",
            c.ordinal_position AS "COL_SORT_ORDER",
            lower(c.table_catalog) AS "DATABASE",
            lower(c.table_schema) AS "SCHEMA",
            CASE
                lower(t.table_type)
                WHEN 'view' THEN 'true'
                ELSE 'false'
            END "IS_VIEW"
        FROM INFORMATION_SCHEMA.COLUMNS AS c
            LEFT JOIN INFORMATION_SCHEMA.TABLES t ON c.TABLE_NAME = t.TABLE_NAME
            AND c.TABLE_SCHEMA = t.TABLE_SCHEMA
        WHERE LOWER(c.table_schema) = LOWER('{schema_name}')
            AND LOWER(c.table_catalog) = LOWER('{database_name}')
        """.format(database_name=database_name, schema_name=schema_name)

    @classmethod
    def query_access_logs_query(cls):
        raise NotImplementedError
        
    @classmethod
    def query_copy_logs_query(cls):
        raise NotImplementedError

class MSSQLSource(SQLAlchemySource):
    def __init__(self, configuration: MSSQLSourceConfiguration):
        self.configuration = configuration
        self.dialect = MSSQLSourceDialect

    def discovery_query(self):
        return TaskUnit(
            request=MSSQLSourceDialect.schema_columns_query(
                database_name=self.configuration.database(),
                schema_name=self.configuration.schema(),
            )
        )