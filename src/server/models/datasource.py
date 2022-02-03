from dataclasses import dataclass
import json
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Table, Text, func

from core.common.drivers.base import DriverDefinition

from . import Base, mapper_registry
from .base import CrudMixin

@dataclass
class TempDatasourceDefinition:
    name: str
    type: str
    configuration: str

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "configuration": self.configuration,
        }

    @classmethod
    def from_dict(cls, ds_dict):
        return cls(
            name=ds_dict['name'],
            type=ds_dict['type'],
            configuration=json.dumps(ds_dict['configuration'])
        )

# TODO: Is this necessary? Is it actually mapped?
# @mapper_registry.mapped

@dataclass
class Datasource(DriverDefinition, Base, CrudMixin):
    # TODO: Abstract id, created_at, updated_at
    __table__ = Table(
        "datasource",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50), unique=True),
        Column("type", String(50)), # TODO: Enum
        Column("configuration", Text), # TODO: Better way to not store JSON-style configuration?

        # TODO: Add updated_on fn
        Column("updated_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
        Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    )

    def to_dict(self):
        obj_dict = super().to_dict()

        obj_dict['id'] = self.id
        obj_dict['updated_at'] = str(self.updated_at)
        obj_dict['created_at'] = str(self.created_at)

        return obj_dict

    def create(self):
        configuration = json.dumps(self.configuration)
        self.configuration = configuration
        super().create()

    # def profile(self):
    #     pass
