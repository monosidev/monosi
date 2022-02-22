import json
from dataclasses import dataclass, field
from datetime import datetime
from mashumaro import DataClassDictMixin
from sqlalchemy import Column, DateTime, Integer, Sequence, String
from sqlalchemy_utils import EncryptedType, JSONType

from core.models import mapper_registry


@mapper_registry.mapped
@dataclass
class DataSource(DataClassDictMixin):
    name: str = field(metadata={"sa": Column(String(100), unique=True)})
    type: str = field(metadata={"sa": Column(String(100))})
    config: str = field(metadata={"sa": Column(JSONType, nullable=False)})

    id: int = field(default=1, metadata={"sa": Column(Integer, Sequence('ds_id_seq'), primary_key=True, autoincrement=True)})
    created_at: datetime = field(default=datetime.now(), metadata={"sa": Column(DateTime(timezone=True), nullable=False)})

    __tablename__ = "msi_sources"
    __sa_dataclass_metadata_key__ = "sa"

    def db_config(self):
        from core.drivers.factory import load_config
        config_cls = load_config(self.type)
        config_obj = config_cls.from_dict(self.config)

        return config_obj

    def db_driver(self):
        config_obj = self.db_config()

        from core.drivers.factory import load_driver
        driver_cls = load_driver(config_obj)
        return driver_cls(config_obj)

