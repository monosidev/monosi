from dataclasses import dataclass, field
from typing import List, Optional
from sqlalchemy.orm import sessionmaker

from core.drivers.base import BaseDriver

from . import mapper_registry
from .workspace import Workspace
from .monitor import MsiMonitor

@dataclass
class Project:
    name: str
    workspace: Workspace
    source_name: str
    singleton: Optional[BaseDriver] = None
    monitors: List[MsiMonitor] = field(default_factory=list)

    # def _save_monitor(self, monitor):
    #     if self.singleton is None:
    #         from core.drivers.factory import load_driver
    #         destination = self.source()
    #         driver_cls = load_driver(destination)
    #         self.singleton = driver_cls(destination)
    #         mapper_registry.metadata.create_all(self.singleton.engine)

    #     try:
    #         Session = sessionmaker(self.singleton.engine)
    #         with Session() as session:
    #             session.add(monitor)
    #             session.commit()
    #             session.expunge_all()
    #             session.close()
    #         self.monitors.append(monitor)
    #     except Exception as e:
    #         raise e

    def add_monitor(self, monitor):
        database, schema, table_name = self.source().fqtn(monitor.table)

        monitor = MsiMonitor(
            database=database.lower(),
            schema=schema.lower(),
            table_name=table_name.lower(),
            timestamp_field=monitor.timestamp_field.lower(),
            type=monitor.type._value_,
            workspace=self.workspace.name,
            source=self.source_name,
        )
        # self._save_monitor(monitor)
        self.monitors.append(monitor)

    def source(self):
        return self.workspace.integrations[self.source_name]

    def destinations(self):
        return [self.source()]

