from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, Sequence, String

from core.models import mapper_registry

@mapper_registry.mapped
@dataclass
class MsiMonitor:
    __tablename__ = "msi_monitors"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, Sequence('id_seq'), primary_key=True)})
    table_name: str = field(default=None, metadata={"sa": Column(String(100))})
    schema: str = field(default=None, metadata={"sa": Column(String(100))})
    database: str = field(default=None, metadata={"sa": Column(String(100))})
    timestamp_field: str = field(default=None, metadata={"sa": Column(String(100))})
    workspace: str = field(default=None, metadata={"sa": Column(String(100))})
    source: str = field(default=None, metadata={"sa": Column(String(100))})
    type: str = field(default=None, metadata={"sa": Column(String(100))})
    # metrics: List[str]
    # columns: List[str]
    # derived: bool

    def fqtn(self):
        return ".".join([self.database, self.schema, self.table_name])
