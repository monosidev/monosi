import json
from typing import Any
from urllib.parse import quote

from ingestion.task import TaskUnit

from .base import (
    SourceConfiguration,
    SQLAlchemySourceDialect,
    SQLAlchemySource,
    MetricsQueryBuilder
)

class ClickhouseMetricsQueryBuilder(MetricsQueryBuilder):
    def _base_query_sample(self, select_sql):
        return """
            SELECT 
                NOW() as WINDOW_START, 
                NOW() as WINDOW_END, 
                COUNT(*) as ROW_COUNT, 
                '{table}' as TABLE_NAME,
                '{database}' as DATABASE_NAME,
                '{database}' as SCHEMA_NAME,

                {select_sql}
            FROM {table};
        """.format(
            select_sql=select_sql,
            table=self.monitor['table_name'],
            schema=self.monitor['schema'],
            database=self.monitor['database'],
        )
    
    def _base_query_backfill(self, select_sql, table, timestamp_field):
        return """
            SELECT 
                DATE_TRUNC({timestamp_field}, HOUR) as WINDOW_START, 
                TIMESTAMP_ADD(DATE_TRUNC({timestamp_field}, HOUR), INTERVAL 1 HOUR) as WINDOW_END, 
                COUNT(*) as ROW_COUNT, 
                {table} as TABLE_NAME,
                {database} as DATABASE_NAME,
                {database} as SCHEMA_NAME,

                {select_sql}
            FROM {table} as c
            WHERE 
                DATE_TRUNC({timestamp_field}, HOUR) >= TIMESTAMP_ADD(NOW(), INTERVAL {minutes_ago} MINUTE)
            GROUP BY WINDOW_START, WINDOW_END
            ORDER BY WINDOW_START ASC;
        """.format(
            select_sql=select_sql,
            table=table,
            timestamp_field=timestamp_field,
            minutes_ago=self.minutes_ago,
            database=self.monitor['database']
        )

class ClickhouseSourceConfiguration(SourceConfiguration):
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
        return "clickhouse+native"

    def connection_string(self) -> str:
        configuration = json.loads(self.configuration)
        connection_string_prefix = self._connection_string_prefix()

        connectionstring = '{prefix}://{user}:{password}@{host}:{port}/{database}'.format(
            prefix=connection_string_prefix,
            user=configuration.get('user'),
            password=configuration.get('password'),
            host=configuration.get('host'),
            port=configuration.get('port'),
            database=configuration.get('database'),
            schema=configuration.get('database')
        )
        
        return connectionstring

class ClickhouseSourceDialect(SQLAlchemySourceDialect):
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
    def _freshness(cls):
        return "(DATE_PART('day', NOW() - MAX({0})) * 24 + DATE_PART('hour', NOW() - MAX({0}))) * 60 + DATE_PART('minute', NOW() - MAX({0}))"        

    @classmethod
    def schema_tables_query(cls, database_name, schema_name):
        raise NotImplementedError

    @classmethod
    def schema_columns_query(cls, database_name, schema_name):
        return """
            SELECT
                lower(c.table_name) AS NAME,
                lower(c.column_name) AS COL_NAME,
                lower(c.data_type) AS COL_TYPE,
                c.ordinal_position AS COL_SORT_ORDER,
                lower(c.table_catalog) AS DATABASE,
                lower(c.table_schema) AS SCHEMA,
                if(t.table_type in (2), 'true', 'false') AS IS_VIEW
            FROM
                INFORMATION_SCHEMA.COLUMNS AS c
            LEFT JOIN
                INFORMATION_SCHEMA.TABLES t
                    ON c.table_name = t.table_name
                    AND c.table_schema = t.table_schema
            WHERE LOWER(c.table_schema) = LOWER('{database_name}')
                AND LOWER(c.table_catalog) = LOWER('{database_name}')
        """.format(database_name=database_name)

    @classmethod
    def query_access_logs_query(cls):
        raise NotImplementedError
        
    @classmethod
    def query_copy_logs_query(cls):
        raise NotImplementedError

class ClickhouseSource(SQLAlchemySource):
    def __init__(self, configuration: ClickhouseSourceConfiguration):
        self.configuration = configuration
        self.dialect = ClickhouseSourceDialect

    def discovery_query(self):
        return TaskUnit(
            request=ClickhouseSourceDialect.schema_columns_query(
                database_name=self.configuration.database(),
                schema_name=self.configuration.schema(),                
            )
        )

