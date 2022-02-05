from dataclasses import dataclass

from sqlalchemy.engine.url import URL

from core.common.drivers.postgres.configuration import PostgresDriverConfiguration

@dataclass
class RedshiftDriverConfiguration(PostgresDriverConfiguration):
    def driver_name(self):
        return "redshift"

    def connection_string(self) -> str:
        url = URL.create(
            drivername='redshift+redshift_connector', # indicate redshift_connector driver and dialect will be used
            host=self.host, # Amazon Redshift host
            port=self.port, # Amazon Redshift port
            database=self.database, # Amazon Redshift database
            username=self.user, # Amazon Redshift username
            password=self.password, # Amazon Redshift password
        )
        return url
