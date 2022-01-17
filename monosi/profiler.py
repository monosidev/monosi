from dataclasses import dataclass
from typing import List

import os
import logging
from monosi.drivers.column import ColumnDataType

from monosi.drivers.column import Column
from monosi.monitors.table import TableMonitor
import monosi.utils.yaml as yaml


def resolve_to_type_from_str(type_str):
    type_str = type_str.lower()
    if 'varchar' in type_str:
        return ColumnDataType.STRING
    elif 'number' in type_str:
        return ColumnDataType.INTEGER
    elif 'date' in type_str or 'timestamp' in type_str:
        return ColumnDataType.DATE

    return ColumnDataType.STRING

@dataclass
class DatabaseTable:
    name: str
    columns: List[Column]

    def timestamp_cols(self):
        t_col_types = [ColumnDataType.DATE, ColumnDataType.DATETIME]
        cols = list(filter(lambda x: x.data_type in t_col_types, self.columns))

        return cols

    def timestamp(self):
        return self.timestamp_cols()[0]

    @classmethod
    def _insert_in_table(cls, tables, name, column):
        if name not in tables:
            table = cls(
                name=name,
                columns=[]
            )
        else:
            table = tables[name]

        table.columns.append(column)
        tables[name] = table

        return tables

    @classmethod
    def from_metadata(cls, metadata):
        tables = {}
        for row in metadata['rows']:
            column = Column(
                name=row['COL_NAME'], 
                data_type=resolve_to_type_from_str(row['COL_TYPE']),
            )
            tables = cls._insert_in_table(tables, row['NAME'], column)

        return tables.values()

BOOTSTRAPPED_MONITOR_PATH = './bootstrapped-monitors'
class Profiler:
    def __init__(self, config):
        self.config = config

    def _retrieve_tables(self):
        from monosi.drivers.factory import load_driver
        driver_cls = load_driver(self.config.config)
        driver = driver_cls(self.config)

        metadata = driver.metadata()
        return DatabaseTable.from_metadata(metadata)

    def _create_definitions(self):
        definitions = []

        tables = self._retrieve_tables()
        for table in tables:
            try:
                monitor = TableMonitor(
                    table=table.name,
                    timestamp_field=table.timestamp().name,
                )
                definition = {
                    'monosi': {
                        'monitors': [monitor.to_dict()]
                    }
                }
                definitions.append(definition)
            except:
                pass
                # logging.warn("Timestamp field could not be found for table")

        return definitions

    def _write_definition(self, definition, monitors_dir=BOOTSTRAPPED_MONITOR_PATH):
        path = os.path.join(monitors_dir, definition['monosi']['monitors'][0]['table'] + ".yaml")
        if not os.path.exists(path):
            yaml.write_file(path, definition)

    def _persist_definitions(self, definitions):
        if not os.path.exists(BOOTSTRAPPED_MONITOR_PATH):
            os.makedirs(BOOTSTRAPPED_MONITOR_PATH)
        self.config.add_monitor_path(BOOTSTRAPPED_MONITOR_PATH)

        for definition in definitions:
            self._write_definition(definition)

    def profile(self):
        definitions = self._create_definitions()
        # TODO: validate definitions
        self._persist_definitions(definitions)


