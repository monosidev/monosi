from dataclasses import dataclass, field
from typing import List

from .workspace import Workspace
from .monitor import MsiMonitor

@dataclass
class Project:
    name: str
    workspace: Workspace
    source_name: str
    monitors: List[MsiMonitor] = field(default_factory=list)

    def add_monitor(self, monitor):
        database, schema, table_name = self.source().fqtn(monitor.table)

        monitor = MsiMonitor(
            database=database,
            schema=schema,
            table_name=table_name,
            timestamp_field=monitor.timestamp_field,
            type=monitor.type._value_,
            workspace=self.workspace.name,
            source=self.source_name,
        )
        self.monitors.append(monitor)

    def source(self):
        return self.workspace.integrations[self.source_name]

    def destinations(self):
        return [self.source()]

