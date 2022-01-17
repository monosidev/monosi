from dataclasses import dataclass, field
from typing import List, Type
import snowflake.connector
from monosi.config.configuration import Configuration
from monosi.events import track_event

from monosi.drivers import BaseDriver, DriverConfig
from monosi.drivers.column import Column, ColumnDataType

from .dialect import SnowflakeDialect

@dataclass
class SnowflakeConfig(DriverConfig):
    account: str = field(default_factory=str)
    password: str = field(default_factory=str)
    user: str = field(default_factory=str)
    warehouse: str = field(default_factory=str)
    host: str = field(default_factory=str)

    def driver_name(self):
        return "snowflake"

    @classmethod
    def retrieve_data(cls, source_dict):
        return {
            'user': source_dict.get('user'),
            'password': source_dict.get('password'),
            'database': source_dict.get('database'),
            'account': source_dict.get('account'),
            'host': cls._host(source_dict.get('account')),
            'warehouse': source_dict.get('warehouse'),
        }

    @classmethod
    def validate(cls, config_dict):
        pass

    @classmethod
    def from_dict(cls, config_dict):
        return cls(**config_dict)
    
    @classmethod
    def _host(cls, account, region=None):
        if region:
            return "{}.{}.snowflakecomputing.com".format(account, region)

        return "{}.snowflakecomputing.com".format(account)
 
    def to_dict(self):
        return {
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'account': self.account,
            'host': self.__class__._host(self.account),
            'warehouse': self.warehouse,
        }

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

def system_tables():
    return ['databases', 'external_tables', 'file_formats', 'functions', 'load_history', 'object_privileges', 'table_privileges', 'pipes', 'procedures', 'referential_constraints', 'replication_databases', 'schemata', 'sequences', 'stages', 'table_constraints', 'table_storage_metrics', 'tables', 'usage_privileges', 'views']

def resolve_to_type_from_str(type_str):
    type_str = type_str.lower()
    if 'varchar' in type_str:
        return ColumnDataType.STRING
    elif 'number' in type_str:
        return ColumnDataType.INTEGER
    elif 'date' in type_str:
        return ColumnDataType.DATE

    return ColumnDataType.STRING

@dataclass
class SnowflakeConfiguration(Configuration):
    config: SnowflakeConfig

class SnowflakeDriver(BaseDriver):
    def __init__(self, config: SnowflakeConfiguration):
        self.config = config.config
        self.dialect = SnowflakeDialect
        try:
            connection_details = self.config.to_dict()
            self._instance = snowflake.connector.connect(
                **connection_details
            )
            track_event(config, action="database_connection_success", label="snowflake")
        except Exception as e:
            track_event(config, action="database_connection_fail", label="snowflake")

    def _before_execute(self, cs):
        if self.config.warehouse is not None: 
            warehouse_sql = "USE WAREHOUSE {}".format(self.config.warehouse) # DANGER
            cs.execute(warehouse_sql)
        if self.config.database is not None: # DANGER
            database_sql = "USE {}".format(self.config.database)
            cs.execute(database_sql)

    def _retrieve_type(self, data_type, scale):
        resolved_type = SNOWFLAKE_TYPES.get(data_type, None)
        if resolved_type == ColumnDataType.STRING and scale is not None and scale > 0:
            resolved_type = ColumnDataType.FLOAT

        return resolved_type

    def _retrieve_results(self, cs):
        column_and_types = [(d[0], self._retrieve_type(d[1], d[5])) for d in cs.description]
        columns = self._create_columns(column_and_types)

        rows = [dict(zip([column.name for column in columns], row)) for row in cs]

        results = {"columns": columns, "rows": rows}
        return results

    def describe_table(self, table) -> List[Column]:
        describe_table_sql = "describe table {}".format(table) # DANGER
        results = self.execute_sql(describe_table_sql)
        
        columns = []
        for row in results['rows']:
            if row['kind'] == 'COLUMN':
                column = Column(row['name'], resolve_to_type_from_str(row['type']))
                columns.append(column)

        return columns

    def execute_sql(self, sql, **params):
        cs = self._instance.cursor()
        results = []
        try:
            self._before_execute(cs)

            cs.execute(sql, params)
            results = self._retrieve_results(cs)
        finally:
            cs.close()

        return results
 
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
        """.format(database=self.config.database)
        results = self.execute_sql(DATABASE_METADATA_SQL)
        filtered_results = {}
        filtered_results['columns'] = results['columns']
        filtered_results['rows'] = []
        rows = results['rows']
        for row in rows:
            if row['NAME'].lower() not in system_tables():
                filtered_results['rows'].append(row)

        return filtered_results


