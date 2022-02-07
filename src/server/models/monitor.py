from dataclasses import dataclass
from typing import Any, Dict
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text, func
import json

from core.common.drivers.base import BaseDriverConfiguration
from core.monitor.models import MonitorDefinition
from core.monitor.models.schedule import Schedule
from core.monitor.tasks.run import RunMonitorTask

from scheduler.job import MonitorJob
from scheduler.models.execution import Execution

from server.scheduler import manager
from core.common.reporter import reporter

from . import Base, mapper_registry
from .base import CrudMixin
from .datasource import Datasource


@dataclass
class Workspace:
    datasources: Dict[str, BaseDriverConfiguration]
    name: str = "default"

    @classmethod
    def from_datasource_definitions(cls, datasource_definitions):
        datasources = {}
        for definition in datasource_definitions:
            datasource = cls._config_from_definition(definition)
            datasources[definition.name] = datasource

        return cls(
            datasources=datasources,
        )

    @classmethod
    def _config_from_definition(cls, definition):
        from core.common.drivers.factory import load_config

        try:
            cls = load_config(definition.type)
            ds_config = json.loads(definition.configuration) # TODO: Fix double call
            try:
                ds_config = json.loads(ds_config)
            except:
                pass
            # ds_config = json.loads(definition.configuration)
            # cls.validate(data)
            config = cls.from_dict(ds_config)
        except Exception as e:
            raise e

        return config

    def get_driver_config(self, source_name: str):
        if source_name not in self.datasources.keys():
            raise Exception("Source {} was not defined or can not be found.".format(source_name))

        return self.datasources[source_name]


# TODO: Is this necessary? Is it actually mapped?
# @mapper_registry.mapped

# @dataclass
# class Schedule(Schedule, Base):
#     __table__ = Table(
#         "schedule",
#         mapper_registry.metadata,
#         Column("id", Integer, primary_key=True),
#         Column("minutes", Integer),
#         Column("type", String(50)),
#     )

@dataclass
class Monitor(MonitorDefinition, Base, CrudMixin):
    # TODO: Abstract id, created_at, updated_at
    __table__ = Table(
        "monitor",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),

        Column("name", String(50)),
        Column("description", Text),
        Column("type", String(50)),
        Column("enabled", Boolean),
        Column("configuration", Text), # TODO: Better way to not store JSON-style configuration?
        # Column('workspace', String), # TODO: Namespace by workspace
        Column('datasource', String, ForeignKey('datasource.name')),
        # Column("schedule", Text), # TODO: Figure out nested dataclass
        Column("schedule_minutes", Integer),
        Column("schedule_type", String(50)),

        # TODO: Add updated_on fn
        Column("updated_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
        Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    )
    # TODO: https://stackoverflow.com/questions/61108811/sqlalchemy-relationship-with-foreignkey-consisting-of-two-columns

    # source = relationship() # TOOD: Declare
    # workspace = relationship()

    def to_dict(self):
        obj_dict = super().to_dict()

        obj_dict['id'] = self.id
        try:
            obj_dict['last_run'] = str(Execution.get_by_job_id(self.id).created_at)
        except:
            pass
        obj_dict['updated_at'] = str(self.updated_at)
        obj_dict['created_at'] = str(self.created_at)

        return obj_dict
        
    def run(self):
        workspace = Workspace.from_datasource_definitions(Datasource.all())
        monitor = self.to_monitor(workspace)
        results = monitor.run()
        print("{} successfully ran.".format(self.name))

    def schedule(self):
        try:
            workspace = Workspace.from_datasource_definitions(Datasource.all())
            monitor = self.to_monitor(workspace)
            task = RunMonitorTask(monitor)
            task.reporter = reporter
            job = MonitorJob(task)
            manager.add_job(job, job_id=self.id)
        except Exception as e:
            raise e

    def create(self):
        try:
            self.schedule()
            return super().create()
        except:
            raise Exception("There was an issue scheduling the monitor during creation.")
        # self.run()

    def delete(self):
        try:
            manager.remove_job(str(self.id))
            Execution.delete_by_job_id(self.id)
            return super().delete()
        except:
            raise Exception("There was an issue removing a scheduled job and could not delete monitor.")

    # TODO: Implementation - should remove route while pending
    # def update(self):
    #     pass



# TODO: Polymorphic association
    # __mapper_args__ = {
    #     'polymorphic_identity':'monitor',
    #     'polymorphic_on':monitor_type,
    #     'with_polymorphic': '*'
    # }
