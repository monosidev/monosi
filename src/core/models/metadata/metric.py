from dataclasses import dataclass, field
from datetime import datetime
from mashumaro import DataClassDictMixin
from sqlalchemy import Column, DateTime, Integer, Sequence, String

from core.models import mapper_registry

@mapper_registry.mapped
@dataclass
class MsiMetric(DataClassDictMixin):
    __tablename__ = "msi_metrics"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, Sequence('id_seq'), primary_key=True)})
    table_name: str = field(default=None, metadata={"sa": Column(String(100))})
    column_name: str = field(default=None, metadata={"sa": Column(String(100))})
    metric: str = field(default=None, metadata={"sa": Column(String(100))})
    value: str = field(default=None, metadata={"sa": Column(String(100))})
    time_window_start: datetime = field(default=None, metadata={"sa": Column(DateTime(timezone=True), nullable=False)})
    time_window_end: datetime = field(default=None, metadata={"sa": Column(DateTime(timezone=True), nullable=False)})
    interval_length_sec: int = field(default=None, metadata={"sa": Column(Integer)})
    created_at: datetime = field(default=datetime.now(), metadata={"sa": Column(DateTime(timezone=True), nullable=False)})
