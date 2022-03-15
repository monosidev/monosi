from dataclasses import dataclass
from typing import Any, List


@dataclass
class TaskUnit:
    request: str

    def run(self, extractor):
        return extractor.run(self)
    
@dataclass
class Task:
    units: List[TaskUnit]
    extractor: Any

    def _run_unit(self, unit: TaskUnit):
        return unit.run(self.extractor)

    def run(self):
        return [self._run_unit(unit) for unit in self.units]
