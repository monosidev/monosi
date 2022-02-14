from dataclasses import dataclass

from core.drivers.base import BaseDriverConfiguration

@dataclass
class SnowflakeDriverConfiguration(BaseDriverConfiguration):
    user: str
    password: str
    warehouse: str
    database: str
    schema: str
    account: str

    def driver_name(self):
        return "snowflake"

    def configuration_schema(self):
        return {}

    def connection_string(self) -> str:
        return 'snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}'.format(
            user=self.user,
            password=self.password,
            account=self.account,
            database=self.database,
            warehouse=self.warehouse,
            schema=self.schema,
        )

    @classmethod
    def from_dict(cls, config_dict):
        return cls(
            user=config_dict.get('user'),
            password=config_dict.get('password'),
            warehouse=config_dict.get('warehouse'),
            database=config_dict.get('database'),
            schema=config_dict.get('schema'),
            account=config_dict.get('account'),
        )

    def to_dict(self):
        return {
            'user': self.user,
            'warehouse': self.warehouse,
            'database': self.database,
            'schema': self.schema,
            'account': self.account,
        }
    
