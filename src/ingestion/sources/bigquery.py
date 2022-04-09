import json

from ingestion.task import TaskUnit

from .base import MetricsQueryBuilder, SourceConfiguration, SQLAlchemySourceDialect, SQLAlchemySource
from sqlalchemy.engine.url import make_url

class BigQueryMetricsQueryBuilder(MetricsQueryBuilder):
    def _base_query_sample(self, select_sql):
        return """
            SELECT 
                CURRENT_TIMESTAMP() as `WINDOW_START`, 
                CURRENT_TIMESTAMP() as `WINDOW_END`, 
                COUNT(*) as `ROW_COUNT`, 
                '{table}' as `TABLE_NAME`,
                '{database}' as `DATABASE_NAME`,
                '{schema}' as `SCHEMA_NAME`,

                {select_sql}
            FROM {database}.{schema}.{table};
        """.format(
            select_sql=select_sql,
            table=self.monitor['table_name'],
            schema=self.monitor['schema'],
            database=self.monitor['database'],
        )

    def _base_query_backfill(self, select_sql, table, timestamp_field):
        return """
            SELECT 
                DATE_TRUNC({timestamp_field}, HOUR) as `WINDOW_START`, 
                TIMESTAMP_ADD(DATE_TRUNC({timestamp_field}, HOUR), INTERVAL 1 HOUR) as `WINDOW_END`, 
                COUNT(*) as `ROW_COUNT`, 
                {table} as `TABLE_NAME`,
                {database} as `DATABASE_NAME`,
                {schema} as `SCHEMA_NAME`,
                {timestamp_field} as `TIMESTAMP_FIELD`,

                {select_sql}
            FROM {schema}.{table} as c
            WHERE 
                DATE_TRUNC({timestamp_field}, HOUR) >= TIMESTAMP_ADD(CURRENT_TIMESTAMP(), INTERVAL {minutes_ago} MINUTE)
            GROUP BY `WINDOW_START`, `WINDOW_END`
            ORDER BY `WINDOW_START` ASC;
        """.format(
            select_sql=select_sql,
            table=table,
            timestamp_field=timestamp_field,
            minutes_ago=self.minutes_ago,
            database=self.monitor['database'],
            schema=self.monitor['schema'],
        )

class BigQuerySourceConfiguration(SourceConfiguration):
    @classmethod
    def validate(cls, configuration):
        raise NotImplementedError

    @classmethod
    def configuration_schema(cls):
        return {
            "type": "object",
            "properties": {
                "project": { "type": "string" },
                "dataset": { "type": "string" },
                "credentials_base64": { "type": "string" },
            },
        }
    
    def _connection_string_prefix(self):
        return "bigquery"

    def connection_string(self) -> str:
        configuration = json.loads(self.configuration)
        connection_string_prefix = self._connection_string_prefix()
        connection_string_base = '{project}/{dataset}'.format(
            project=configuration.get('project'),
            dataset=configuration.get('dataset'),
        )
        connection_string_params = '?credentials_base64={credentials_base64}'.format(
            credentials_base64=configuration.get('credentials_base64')
        )

        connection_string = '{connection_string_prefix}://{connection_string_base}{connection_string_params}'.format(
            connection_string_prefix=connection_string_prefix,
            connection_string_base=connection_string_base,
            connection_string_params=connection_string_params
        )

        return make_url(connection_string)


    def database(self):
        return json.loads(self.configuration).get("project")

    def schema(self):
        return json.loads(self.configuration).get('dataset')

    @property
    def type(self):
        return "bigquery"

class BigQuerySourceDialect(SQLAlchemySourceDialect):
    @classmethod
    def _numeric_std(cls):
        return "STDDEV(CAST({} as FLOAT64))"

    @classmethod
    def _std_length(cls):
        return "STDDEV(CAST(LENGTH({}) as FLOAT64))"
    
    @classmethod
    def _text_int_rate(cls):
        return "SUM(ARRAY_LENGTH(REGEXP_EXTRACT_ALL(CAST({} AS STRING), r'^([-+]?[0-9]+)$'))) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _text_number_rate(cls):
        return "SUM(ARRAY_LENGTH(REGEXP_EXTRACT_ALL(CAST({} AS STRING), r'^[\+\-]?\d*\.?\d+(?:[Ee][\+\-]?\d+)?$'))) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _text_uuid_rate(cls):
        return "SUM(ARRAY_LENGTH(REGEXP_EXTRACT_ALL(CAST({} AS STRING2), r'^([0-9a-fA-F]{{8}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{12}})$'))) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _text_all_spaces_rate(cls):
        return "SUM(ARRAY_LENGTH(REGEXP_EXTRACT_ALL(CAST({} AS STRING), r'^\s*$'))) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _text_null_keyword_rate(cls):
        return "SUM(CASE WHEN UPPER(CAST({} as STRING)) IS NULL THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _zero_rate(cls): # TODO: ?
        return "SUM(CASE WHEN UPPER(CAST({} as STRING)) IS NULL THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _negative_rate(cls):
        return "SUM(CASE WHEN {} < 0 THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC)"

    @classmethod
    def _completeness(cls):
        return "COUNT({}) / CAST(COUNT(*) AS NUMERIC)"
    
    @classmethod
    def _freshness(cls):
        return "TIMESTAMP_DIFF(MAX({}), CURRENT_TIMESTAMP, MINUTE)"

    @classmethod
    def table_metrics_query(cls, monitor, discovery_data, minutes_ago):
        builder = BigQueryMetricsQueryBuilder(cls, monitor, discovery_data, minutes_ago)
        query = builder.compile()
        return query


    @classmethod
    def schema_columns_query(cls, database_name, schema_name):
        return """
        SELECT lower(c.table_name) AS `NAME`,
            lower(c.column_name) AS `COL_NAME`,
            lower(c.data_type) AS `COL_TYPE`,
            c.ordinal_position AS `COL_SORT_ORDER`,
            lower(c.table_catalog) AS `DATABASE`,
            lower(c.table_schema) AS `SCHEMA`,
            CASE
                lower(t.table_type)
                WHEN 'view' THEN 'true'
                ELSE 'false'
            END `IS_VIEW`
        FROM {schema_name}.INFORMATION_SCHEMA.COLUMNS AS c
            LEFT JOIN {schema_name}.INFORMATION_SCHEMA.TABLES t ON c.TABLE_NAME = t.TABLE_NAME
            AND c.TABLE_SCHEMA = t.TABLE_SCHEMA
        WHERE LOWER(c.table_schema) = LOWER('{schema_name}')
            AND LOWER(c.table_catalog) = LOWER('{database_name}')
        """.format(database_name=database_name, schema_name=schema_name)

class BigQuerySource(SQLAlchemySource):
    def __init__(self, configuration: BigQuerySourceConfiguration):
        self.configuration = configuration
        self.dialect = BigQuerySourceDialect

    def discovery_query(self):
        return TaskUnit(
            request=BigQuerySourceDialect.schema_columns_query(
                database_name=self.configuration.database(),
                schema_name=self.configuration.schema(),
            )
        )

