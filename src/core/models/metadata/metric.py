from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class MsiMetric:
    table_name: str
    column_name: str
    metric: str
    value: str # TODO: Update?
    time_window_start: datetime
    time_window_end: datetime
    interval_length_sec: int
    created_at: datetime = field(default_factory=lambda: datetime.now())
    id: int = 1
