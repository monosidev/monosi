from dataclasses import dataclass, field
from datetime import datetime
from mashumaro import DataClassDictMixin
from sqlalchemy import Column, Integer, Sequence, Text, DateTime
from typing import Optional

from sqlalchemy.sql.functions import func
from scheduler import constants

from . import mapper_registry

@mapper_registry.mapped
@dataclass
class Execution(DataClassDictMixin):
    job_id: str = field(metadata={"sa": Column(Text)})
    state: int = field(metadata={"sa": Column(Integer)})
    result: Optional[str] = field(metadata={"sa": Column(Text, nullable=True)})

    id: int = field(default=None, metadata={"sa": Column(Integer, Sequence('ds_id_seq'), primary_key=True, autoincrement=True)})
    datasource_id: int = field(default=None, metadata={"sa": Column(Integer, nullable=True)})
    created_at: datetime = field(default=None, metadata={"sa": Column(DateTime(timezone=True), nullable=False, server_default=func.now())})
    updated_at: datetime = field(default=None, metadata={"sa": Column(DateTime(timezone=True), nullable=False, server_default=func.now())})

    __tablename__ = "msi_executions"
    __sa_dataclass_metadata_key__ = "sa"
