from dataclasses import dataclass

from core.common.drivers.base import BaseDriverConfiguration

@dataclass
class PostgresDriverConfiguration(BaseDriverConfiguration):
    user: str
    password: str
    host: str
    database: str
    port: int = 5432

    def driver_name(self):
        return "postgres"

    def connection_string(self) -> str:
        return 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )

    @classmethod
    def from_dict(cls, config_dict):
        return cls(
            user=config_dict.get('user'),
            password=config_dict.get('password'),
            database=config_dict.get('database'),
            host=config_dict.get('host'),
            port=config_dict.get('port'),
        )

    def to_dict(self):
        return {
            'user': self.user,
            'database': self.database,
            'host': self.host,
            'port': self.port,
        }
    