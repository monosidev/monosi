from dataclasses import dataclass

@dataclass
class MsiMonitor:
    table_name: str
    schema: str
    database: str
    timestamp_field: str
    workspace: str
    source: str
    type: str
    # metrics: List[str]
    # columns: List[str]
    # derived: bool

