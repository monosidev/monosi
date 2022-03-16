from dataclasses import dataclass, field
from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    Sequence,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import registry
from sqlalchemy.sql import func
from sqlalchemy_utils import JSONType
from mashumaro import DataClassDictMixin


mapper_registry = registry()

@mapper_registry.mapped
@dataclass
class DataSource(DataClassDictMixin):
    name: str = field(metadata={"sa": Column(String(100), unique=True)})
    type: str = field(metadata={"sa": Column(String(100))})
    config: str = field(metadata={"sa": Column(JSONType, nullable=False)})

    id: int = field(default=None, metadata={"sa": Column(Integer, Sequence('ds_id_seq'), primary_key=True, autoincrement=True)})
    created_at: datetime = field(default=datetime.now(), metadata={"sa": Column(DateTime(timezone=True), nullable=False)})

    __tablename__ = "msi_sources"
    __sa_dataclass_metadata_key__ = "sa"

    def db_config(self):
        raise NotImplementedError

    def db_driver(self):
        raise NotImplementedError

@mapper_registry.mapped
@dataclass
class Integration(DataClassDictMixin):
    __tablename__ = "msi_integrations"
    __sa_dataclass_metadata_key__ = "sa"

    name: str = field(metadata={"sa": Column(String(100), unique=True)})
    type: str = field(metadata={"sa": Column(String(100))})
    config: str = field(metadata={"sa": Column(JSONType, nullable=False)})

    id: int = field(default=None, metadata={"sa": Column(Integer, Sequence('integ_id_seq'), primary_key=True, autoincrement=True)})
    created_at: datetime = field(default=datetime.now(), metadata={"sa": Column(DateTime(timezone=True), nullable=False)})

    def send(self, message):
        raise NotImplementedError

@mapper_registry.mapped
@dataclass
class Metric(DataClassDictMixin):
    __tablename__ = "msi_metrics"
    __sa_dataclass_metadata_key__ = "sa"
    __table_args__ = (
        UniqueConstraint('table_name', 'schema', 'database', 'time_window_start', 'time_window_end', 'column_name', 'metric'),
    )

    table_name: str = field(default=None, metadata={"sa": Column(String(100))})
    schema: str = field(default=None, metadata={"sa": Column(String(100))})
    database: str = field(default=None, metadata={"sa": Column(String(100))})
    column_name: str = field(default=None, metadata={"sa": Column(String(100))})
    metric: str = field(default=None, metadata={"sa": Column(String(100))})
    value: str = field(default=None, metadata={"sa": Column(String(100))})
    time_window_start: datetime = field(default=None, metadata={"sa": Column(DateTime(timezone=True), nullable=False)})
    time_window_end: datetime = field(default=None, metadata={"sa": Column(DateTime(timezone=True), nullable=False)})
    interval_length_sec: int = field(default=None, metadata={"sa": Column(Integer)})

    id: int = field(default=None, metadata={"sa": Column(Integer, Sequence('metric_id_seq'), primary_key=True, autoincrement=True)})
    created_at: datetime = field(default=datetime.now(), metadata={"sa": Column(DateTime(timezone=True), nullable=False, server_default=func.now())})

@mapper_registry.mapped
@dataclass
class Monitor(DataClassDictMixin):
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
    days_ago: int = field(default=100, metadata={"sa": Column(Integer)})
    type: str = field(default=None, metadata={"sa": Column(String(100))})
    
    id: int = field(default=None, metadata={"sa": Column(Integer, Sequence('integ_id_seq'), primary_key=True, autoincrement=True)})
    created_at: datetime = field(default=datetime.now(), metadata={"sa": Column(DateTime(timezone=True), nullable=False)})


    def fqtn(self):
        return ".".join([self.database, self.schema, self.table_name]).lower()

@mapper_registry.mapped
@dataclass
class ZScore(DataClassDictMixin):
    __tablename__ = "msi_zscores"
    __sa_dataclass_metadata_key__ = "sa"

    metric_id: int = field(default=None, metadata={"sa": Column(Integer, unique=True)})
    expected_range_start: float = field(default=None, metadata={"sa": Column(Float)})
    expected_range_end: float = field(default=None, metadata={"sa": Column(Float)})
    error: bool = field(default=None, metadata={"sa": Column(Boolean)})
    zscore: float = field(default=None, metadata={"sa": Column(Float)})

    id: int = field(default=None, metadata={"sa": Column(Integer, Sequence('zscore_id_seq'), primary_key=True, autoincrement=True)})
