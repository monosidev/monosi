import json
from typing import Any
from urllib.parse import quote

from .base import (
    SourceConfiguration,
    SQLAlchemySourceDialect,
    SQLAlchemySource,
    SQLAlchemyExtractor
)

class SnowflakeSourceConfiguration(SourceConfiguration):
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
            password=quote(configuration.get('password')),
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
    def schema_tables_query(cls, database_name, schema_name):
        return """
            SELECT 
              TABLE_CATALOG, 
              TABLE_SCHEMA,
              TABLE_NAME, 
              TABLE_OWNER, 
              TABLE_TYPE, 
              IS_TRANSIENT, 
              RETENTION_TIME, 
              AUTO_CLUSTERING_ON, 
              COMMENT 
            FROM {database_name}.information_schema.tables 
            WHERE 
              table_schema NOT IN ('INFORMATION_SCHEMA') 
              AND TABLE_TYPE NOT IN ('VIEW', 'EXTERNAL TABLE') 
              AND LOWER( TABLE_SCHEMA ) = LOWER('{schema_name}')
            ORDER BY TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME;
        """.format(database_name=database_name, schema_name=schema_name)

    @classmethod
    def schema_columns_query(cls, database_name, schema_name):
        return """
            SELECT
                lower(c.table_name) AS NAME,
                lower(c.column_name) AS COL_NAME,
                lower(c.data_type) AS COL_TYPE,
                c.comment AS COL_DESCRIPTION,
                lower(c.ordinal_position) AS COL_SORT_ORDER,
                lower(c.table_catalog) AS DATABASE,
                lower(c.table_schema) AS SCHEMA,
                t.comment AS DESCRIPTION,
                decode(lower(t.table_type), 'view', 'true', 'false') AS IS_VIEW
            FROM
                {database_name}.INFORMATION_SCHEMA.COLUMNS AS c
            LEFT JOIN
                {database_name}.INFORMATION_SCHEMA.TABLES t
                    ON c.TABLE_NAME = t.TABLE_NAME
                    AND c.TABLE_SCHEMA = t.TABLE_SCHEMA
            WHERE LOWER( schema ) = LOWER('{schema_name}')
        """.format(database_name=database_name, schema_name=schema_name)

    @classmethod
    def access_logs_query(cls):
        return """
            SELECT 
                "QUERY_TEXT", 
                "DATABASE_NAME", 
                "SCHEMA_NAME", 
                "QUERY_TYPE", 
                "USER_NAME", 
                "ROLE_NAME", 
                "EXECUTION_STATUS", 
                "START_TIME", 
                "END_TIME", 
                "TOTAL_ELAPSED_TIME", 
                "BYTES_SCANNED", 
                "ROWS_PRODUCED", 
                "SESSION_ID", 
                "QUERY_ID", 
                "QUERY_TAG", 
                "WAREHOUSE_NAME", 
                "ROWS_INSERTED", 
                "ROWS_UPDATED", 
                "ROWS_DELETED", 
                "ROWS_UNLOADED" 
            FROM snowflake.account_usage.query_history 
            WHERE 
                start_time BETWEEN to_timestamp_ltz('2021-01-01 00:00:00.000000+00:00') AND to_timestamp_ltz('2021-01-01 01:00:00.000000+00:00') 
                AND QUERY_TYPE NOT IN ('DESCRIBE', 'SHOW') 
                AND (DATABASE_NAME IS NULL OR DATABASE_NAME NOT IN ('UTIL_DB', 'SNOWFLAKE')) 
                AND ERROR_CODE is NULL 
            ORDER BY start_time DESC;
        """
        
    @classmethod
    def copy_and_load_logs_query(cls):
        return """
            SELECT 
                "FILE_NAME", 
                "STAGE_LOCATION", 
                "LAST_LOAD_TIME", 
                "ROW_COUNT", 
                "FILE_SIZE", 
                "ERROR_COUNT", 
                "STATUS", 
                "TABLE_CATALOG_NAME", 
                "TABLE_SCHEMA_NAME", 
                "TABLE_NAME", 
                "PIPE_CATALOG_NAME", 
                "PIPE_SCHEMA_NAME", 
                "PIPE_NAME", 
                "PIPE_RECEIVED_TIME" 
            FROM snowflake.account_usage.copy_history 
            WHERE 
                LAST_LOAD_TIME between to_timestamp_ltz('2021-01-01 00:00:00.000000+00:00') AND to_timestamp_ltz('2021-01-01 01:00:00.000000+00:00')
                AND STATUS != 'load failed' 
            ORDER BY LAST_LOAD_TIME DESC;
        """

class SnowflakeSourceExtractor(SQLAlchemyExtractor):
    def discovery_query(self):
        return SnowflakeSourceDialect.schema_columns_query(
            database_name=self.configuration.database(),
            schema_name=self.configuration.schema(),
        )

class SnowflakeSource(SQLAlchemySource):
    def __init__(self, configuration: SnowflakeSourceConfiguration):
        self.configuration = configuration
        self.dialect = SnowflakeSourceDialect

    def extractor(self):
        return SnowflakeSourceExtractor(self.configuration)

