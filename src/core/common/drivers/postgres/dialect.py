from core.common.drivers.base import BaseDialect

class PostgresDialect(BaseDialect):
    @classmethod
    def numeric_std(cls):
        return "STDDEV(CAST({} as double precision))"
    
    @classmethod
    def text_int_rate(cls):
        return "SUM(CASE WHEN CAST({} AS varchar) ~ '^([-+]?[0-9]+)$' THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def text_number_rate(cls):
        return "SUM(CASE WHEN CAST({} AS varchar) ~ '^([-+]?[0-9]*[.]?[0-9]+([eE][-+]?[0-9]+)?)$' THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def text_uuid_rate(cls):
        return "SUM(CASE WHEN CAST({} AS varchar) ~ '^([0-9a-fA-F]{{8}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{12}})$' THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def text_all_spaces_rate(cls):
        return "SUM(CASE WHEN CAST({} AS varchar) ~ '^(\\\\s+)$' THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def text_null_keyword_rate(cls):
        return "SUM(CASE WHEN UPPER(CAST({} as varchar)) IN ('NULL', 'NONE', 'NIL', 'NOTHING') THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def zero_rate(cls): # TODO: ?
        return "SUM(CASE WHEN UPPER(CAST({} as varchar)) IN ('NULL', 'NONE', 'NIL', 'NOTHING') THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def negative_rate(cls):
        return "SUM(CASE WHEN {} < 0 THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def completeness(cls):
        return "COUNT({}) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def metadata_query(cls):
        return """
        SELECT
            lower(c.table_name) AS name,
            lower(c.column_name) AS COL_NAME,
            lower(c.data_type) AS COL_TYPE,
            ordinal_position AS COL_SORT_ORDER, 
            lower(c.table_catalog) AS database,
            lower(c.table_schema) AS schema
        FROM
            INFORMATION_SCHEMA.COLUMNS AS c
        LEFT JOIN
            INFORMATION_SCHEMA.TABLES t
                ON c.TABLE_NAME = t.TABLE_NAME
                AND c.TABLE_SCHEMA = t.TABLE_SCHEMA
        WHERE LOWER( c.table_name ) = '{table_name}'
          AND LOWER( c.table_schema ) = '{schema_name}'
          AND LOWER( c.table_catalog ) = '{database_name}'"""

    @classmethod
    def table_query(cls):
        return """
            SELECT 
                DATE_TRUNC('HOUR', {timestamp_field}) as window_start, 
                DATE_TRUNC('HOUR', {timestamp_field}) + interval '1 hour' as window_end,

                COUNT(*) as row_count,

                {select_sql}

            FROM {table}
            WHERE 
                DATE_TRUNC('HOUR', {timestamp_field}) >= CURRENT_TIMESTAMP + interval '{minutes_ago} minutes' 
            GROUP BY window_start, window_end 
            ORDER BY window_start ASC;
        """
