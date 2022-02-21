from dataclasses import dataclass

from dataclasses import dataclass, field
from sqlalchemy import Boolean, Column, Float, Integer, Sequence
from mashumaro import DataClassDictMixin

from core.models import mapper_registry

@mapper_registry.mapped
@dataclass
class ZScore(DataClassDictMixin):
    __tablename__ = "msi_zscores"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(default=None, metadata={"sa": Column(Integer, Sequence('zscore_id_seq'), primary_key=True, autoincrement=True)})
    metric_id: int = field(default=None, metadata={"sa": Column(Integer, unique=True)})
    expected_range_start: float = field(default=None, metadata={"sa": Column(Float)})
    expected_range_end: float = field(default=None, metadata={"sa": Column(Float)})
    error: bool = field(default=None, metadata={"sa": Column(Boolean)})
    zscore: float = field(default=None, metadata={"sa": Column(Float)})
