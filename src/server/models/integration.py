from dataclasses import dataclass
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Table, Text, func

from core.common.reporter import reporter
from server.integrations.base import IntegrationDefinition
from server.integrations.slack import SlackIntegration

from . import Base, mapper_registry
from .base import CrudMixin


# TODO: Is this necessary? Is it actually mapped?
# @mapper_registry.mapped

@dataclass
class Integration(IntegrationDefinition, Base, CrudMixin):
    # TODO: Abstract id, created_at, updated_at
    __table__ = Table(
        "integration",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),

        Column("name", String(50)),
        Column("type", String(50)), # TODO: Enum
        Column("enabled", Boolean),
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

    def register(self):
        # TODO: Support more than slack
        integration = SlackIntegration(
            name=self.name,
            enabled=self.enabled,
            configuration=self.configuration,
        )
        reporter.register_listener(integration)

    def create(self):
        super().create()
        self.register()
