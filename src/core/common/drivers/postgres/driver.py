from typing import Type

from core.common.drivers.base import BaseDialect, BaseSqlAlchemyDriver
from core.common.drivers.column import ColumnDataType

from .configuration import PostgresDriverConfiguration
from .dialect import PostgresDialect


POSTGRES_SYSTEM_TABLES = [
    'pg_aggregate',
    'pg_am',
    'pg_amop',
    'pg_amproc',
    'pg_attrdef',
    'pg_attribute',
    'pg_authid',
    'pg_auth_members',
    'pg_cast',
    'pg_class',
    'pg_constraint',
    'pg_collation',
    'pg_conversion',
    'pg_database',
    'pg_db_role_setting',
    'pg_default_acl',
    'pg_depend',
    'pg_description',
    'pg_enum',
    'pg_extension',
    'pg_foreign_data_wrapper',
    'pg_foreign_server',
    'pg_foreign_table',
    'pg_index',
    'pg_inherits',
    'pg_language',
    'pg_largeobject',
    'pg_largeobject_metadata',
    'pg_namespace',
    'pg_opclass',
    'pg_operator',
    'pg_opfamily',
    'pg_pltemplate',
    'pg_proc',
    'pg_rewrite',
    'pg_seclabel',
    'pg_shdepend',
    'pg_shdescription',
    'pg_statistic',
    'pg_tablespace',
    'pg_trigger',
    'pg_ts_config',
    'pg_ts_config_map',
    'pg_ts_dict',
    'pg_ts_parser',
    'pg_ts_template',
    'pg_type',
    'pg_user_mapping',
    # System Views
    'pg_available_extensions',
    'pg_available_extension_versions',
    'pg_cursors',
    'pg_group',
    'pg_indexes',
    'pg_locks',
    'pg_prepared_statements',
    'pg_prepared_xacts',
    'pg_roles',
    'pg_rules',
    'pg_seclabels',
    'pg_settings',
    'pg_shadow',
    'pg_stats',
    'pg_tables',
    'pg_timezone_abbrevs',
    'pg_timezone_names',
    'pg_user',
    'pg_user_mappings',
    'pg_views',

    'information_schema',
    'pg_catalog',
]

POSTGRES_TYPES = {
    
}

class PostgresDriver(BaseSqlAlchemyDriver):
    configuration: PostgresDriverConfiguration
    dialect: Type[BaseDialect] = PostgresDialect

    def _retrieve_type(self, type_code, scale):
        resolved_type = POSTGRES_TYPES.get(type_code, None)
        if resolved_type == ColumnDataType.STRING and scale is not None and scale > 0:
            resolved_type = ColumnDataType.FLOAT

        return resolved_type

    @staticmethod
    def _filter_metadata(results):
        filtered_results = {}
        filtered_results['columns'] = results['columns']
        filtered_results['rows'] = []
        rows = results['rows']
        for row in rows:
            if row['NAME'].lower() not in POSTGRES_SYSTEM_TABLES:
                filtered_results['rows'].append(row)

        return filtered_results

    def metadata(self):
        DATABASE_METADATA_SQL = """
        SELECT
            lower(c.table_name) AS NAME,
            lower(c.column_name) AS COL_NAME,
            lower(c.data_type) AS COL_TYPE,
            ordinal_position AS COL_SORT_ORDER, 
            lower(c.table_catalog) AS DATABASE,
            lower(c.table_schema) AS SCHEMA
        FROM
            INFORMATION_SCHEMA.COLUMNS AS c
        LEFT JOIN
            INFORMATION_SCHEMA.TABLES t
                ON c.TABLE_NAME = t.TABLE_NAME
                AND c.TABLE_SCHEMA = t.TABLE_SCHEMA;
        """

        results = self.execute(DATABASE_METADATA_SQL)
        filtered_results = self._filter_metadata(results)

        return filtered_results

