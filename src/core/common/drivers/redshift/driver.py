from dataclasses import dataclass

from core.common.drivers.postgres.driver import PostgresDriver

from .configuration import RedshiftDriverConfiguration
from .dialect import RedshiftDialect


class RedshiftDriver(PostgresDriver):
    dialect: RedshiftDialect
    configuration: RedshiftDriverConfiguration

    def _retrieve_results(self, cs):
        column_and_types = [(d[0].decode("utf-8"), self._retrieve_type(d[1], None)) for d in cs.cursor.description]
        columns = self._create_columns(column_and_types)
        rows = [dict(zip([col.name for col in columns], row)) for row in cs.fetchall()]

        return {
            "columns": columns, 
            "rows": rows,
        }
