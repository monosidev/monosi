from dataclasses import dataclass
from datetime import datetime


@dataclass
class MsiJob:
    table_name: str
    column_name: str
    monitor_name: str
    status: int
    created_at: datetime

