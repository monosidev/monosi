from dataclasses import dataclass, field
from datetime import datetime
from mashumaro import DataClassDictMixin
from sqlalchemy import Column, DateTime, Integer, Sequence, String
from sqlalchemy_utils import EncryptedType, JSONType

from core.models import mapper_registry
from core.models.integrations.slack import SlackIntegration


@mapper_registry.mapped
@dataclass
class Integration(DataClassDictMixin):
    name: str = field(metadata={"sa": Column(String(100), unique=True)})
    type: str = field(metadata={"sa": Column(String(100))})
    config: str = field(metadata={"sa": Column(JSONType, nullable=False)})

    id: int = field(default=1, metadata={"sa": Column(Integer, Sequence('integ_id_seq'), primary_key=True, autoincrement=True)})
    created_at: datetime = field(default=datetime.now(), metadata={"sa": Column(DateTime(timezone=True), nullable=False)})

    __tablename__ = "msi_integrations"
    __sa_dataclass_metadata_key__ = "sa"

    def send(self, message):
        SlackIntegration.send(message, self.config)

