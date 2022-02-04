from core.common.drivers.base import BaseDialect

class SnowflakeDialect(BaseDialect):
    @classmethod
    def text_int_rate(cls):
        return "SUM(IFF(REGEXP_COUNT(TO_VARCHAR({}), '^([-+]?[0-9]+)$', 1, 'i') != 0, 1, 0)) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def text_number_rate(cls):
        return "SUM(IFF(REGEXP_COUNT(TO_VARCHAR({}), '^([-+]?[0-9]*[.]?[0-9]+([eE][-+]?[0-9]+)?)$', 1, 'i') != 0, 1, 0)) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def text_uuid_rate(cls):
        return "SUM(IFF(REGEXP_COUNT(TO_VARCHAR({}), '^([0-9a-fA-F]{{8}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{12}})$', 1, 'i') != 0, 1, 0)) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def text_all_spaces_rate(cls):
        return "SUM(IFF(REGEXP_COUNT(TO_VARCHAR({}), '^(\\\\s+)$', 1, 'i') != 0, 1, 0)) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def text_null_keyword_rate(cls):
        return "SUM(IFF(UPPER({}) IN ('NULL', 'NONE', 'NIL', 'NOTHING'), 1, 0)) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def zero_rate(cls):
        return "SUM(IFF(UPPER({}) IN ('NULL', 'NONE', 'NIL', 'NOTHING'), 1, 0)) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def negative_rate(cls):
        return "SUM(IFF({} < 0, 1, 0)) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def completeness(cls):
        return "COUNT({}) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def metadata_query(cls):
        return """
            SELECT
                lower(c.table_name) AS name,
                lower(c.column_name) AS col_name,
                lower(c.data_type) AS col_type,
                c.comment AS col_description,
                lower(c.ordinal_position) AS col_sort_order,
                lower(c.table_catalog) AS database,
                lower(c.table_schema) AS schema,
                t.comment AS description,
                decode(lower(t.table_type), 'view', 'true', 'false') AS is_view
            FROM
                {database_name}.INFORMATION_SCHEMA.COLUMNS AS c
            LEFT JOIN
                {database_name}.INFORMATION_SCHEMA.TABLES t
                    ON c.TABLE_NAME = t.TABLE_NAME
                    AND c.TABLE_SCHEMA = t.TABLE_SCHEMA
            WHERE LOWER( name ) = '{table_name}'
              AND LOWER( schema ) = '{schema_name}'
        """

    @classmethod
    def table_query(cls):
        return """
            SELECT 
                DATE_TRUNC('HOUR', {timestamp_field}) as window_start, 
                DATEADD(hr, 1, DATE_TRUNC('HOUR', {timestamp_field})) as window_end, 

                COUNT(*) as row_count, 

                {select_sql}

            FROM {table}
            WHERE 
                DATE_TRUNC('HOUR', {timestamp_field}) >= DATEADD(minute, {minutes_ago}, CURRENT_TIMESTAMP()) 
            GROUP BY window_start, window_end 
            ORDER BY window_start ASC;
        """

