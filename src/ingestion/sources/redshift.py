import json

from .postgresql import PostgreSQLSource, PostgreSQLSourceConfiguration

class RedshiftSourceConfiguration(PostgreSQLSourceConfiguration):
    def _connection_string_prefix(self) -> str:
        return "redshift+psycopg2"

    @property
    def type(self):
        return "redshift"

class RedshiftSource(PostgreSQLSource):
    pass

# NOTE: Classes not currently used

# class RedshiftSourceDialect(PostgreSQLSourceDialect):
    # TODO: Potential dialect override necessary
    # pass

# class RedshiftSourceExtractor(PostgreSQLSourceExtractor):
#     pass