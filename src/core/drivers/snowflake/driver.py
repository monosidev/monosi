from dataclasses import dataclass
from typing import Type

from core.common.drivers.base import BaseDialect, BaseSqlAlchemyDriver
from core.common.drivers.column import ColumnDataType

from .configuration import SnowflakeDriverConfiguration
from .dialect import SnowflakeDialect


SNOWFLAKE_TYPES = {
    0: ColumnDataType.INTEGER,
    1: ColumnDataType.FLOAT,
    2: ColumnDataType.STRING,
    3: ColumnDataType.DATE,
    4: ColumnDataType.DATETIME,
    5: ColumnDataType.STRING,
    6: ColumnDataType.DATETIME,
    7: ColumnDataType.DATETIME,
    8: ColumnDataType.DATETIME,
    13: ColumnDataType.BOOLEAN,
}

SNOWFLAKE_SYSTEM_TABLES = [
    'databases',
    'external_tables',
    'file_formats',
    'functions',
    'load_history',
    'object_privileges',
    'table_privileges',
    'pipes',
    'procedures',
    'referential_constraints',
    'replication_databases',
    'schemata',
    'sequences',
    'stages',
    'table_constraints',
    'table_storage_metrics',
    'tables',
    'usage_privileges',
    'views'
]


@dataclass
class SnowflakeDriver(BaseSqlAlchemyDriver):
    def __init__(self, configuration: SnowflakeDriverConfiguration):
        self.configuration: SnowflakeDriverConfiguration = configuration
        self.dialect: Type[BaseDialect] = SnowflakeDialect
        self.connection = self._open()

    def _retrieve_type(self, type_code, scale):
        resolved_type = SNOWFLAKE_TYPES.get(type_code, None)
        if resolved_type == ColumnDataType.STRING and scale is not None and scale > 0:
            resolved_type = ColumnDataType.FLOAT

        return resolved_type

    def _before_execute(self):
        if not self.connection:
            return

        warehouse_sql = 'USE WAREHOUSE {}'.format(self.configuration.warehouse)
        database_sql = 'USE {}'.format(self.configuration.database)

        try:
            self.connection.execute(warehouse_sql)
            self.connection.execute(database_sql)
        except Exception as e:
            raise e

    @staticmethod
    def _filter_metadata(results):
        filtered_results = {}
        filtered_results['columns'] = results['columns']
        filtered_results['rows'] = []
        rows = results['rows']
        for row in rows:
            if row['NAME'].lower() not in SNOWFLAKE_SYSTEM_TABLES:
                filtered_results['rows'].append(row)

        return filtered_results

    def metadata(self):
        DATABASE_METADATA_SQL = """
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
            {database}.INFORMATION_SCHEMA.COLUMNS AS c
        LEFT JOIN
            {database}.INFORMATION_SCHEMA.TABLES t
                ON c.TABLE_NAME = t.TABLE_NAME
                AND c.TABLE_SCHEMA = t.TABLE_SCHEMA;
        """.format(database=self.configuration.database)

        results = self.execute(DATABASE_METADATA_SQL)
        filtered_results = self._filter_metadata(results)

        return filtered_results

