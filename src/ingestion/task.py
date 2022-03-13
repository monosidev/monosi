from dataclasses import dataclass
from typing import List

from .sources import Extractor


@dataclass
class TaskUnit:
    request: str

    def run(self, extractor: Extractor):
        return extractor.run(self.request)
    
@dataclass
class Task:
    units: List[TaskUnit]
    extractor: Extractor

    def _run_unit(self, unit: TaskUnit):
        return unit.run(self.extractor)

    def run(self):
        return [self._run_unit(unit) for unit in self.units]
