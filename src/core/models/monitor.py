from dataclasses import dataclass, field
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Sequence, String, UniqueConstraint
from mashumaro import DataClassDictMixin

from core.models import mapper_registry

@mapper_registry.mapped
@dataclass
class MsiMonitor(DataClassDictMixin):
    __tablename__ = "msi_monitors"
    __sa_dataclass_metadata_key__ = "sa"
    __table_args__ = (
        UniqueConstraint('table_name', 'schema', 'database', 'timestamp_field', 'source', 'type'),
    )

    table_name: str = field(default=None, metadata={"sa": Column(String(100), nullable=False)})
    schema: str = field(default=None, metadata={"sa": Column(String(100), nullable=False)})
    database: str = field(default=None, metadata={"sa": Column(String(100))})
    timestamp_field: str = field(default=None, metadata={"sa": Column(String(100))})
    workspace: str = field(default=None, metadata={"sa": Column(String(100))})
    source: str = field(default=None, metadata={"sa": Column(String(100))})
    type: str = field(default=None, metadata={"sa": Column(String(100))})
    
    id: int = field(default=None, metadata={"sa": Column(Integer, Sequence('integ_id_seq'), primary_key=True, autoincrement=True)})
    created_at: datetime = field(default=datetime.now(), metadata={"sa": Column(DateTime(timezone=True), nullable=False)})
    # metrics: List[str]
    # columns: List[str]
    # derived: bool

    def fqtn(self):
        return ".".join([self.database, self.schema, self.table_name]).lower()
