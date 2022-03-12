from dataclasses import dataclass
from typing import List

from .sources import Extractor


@dataclass
class TaskUnit:
    request: str
    
@dataclass
class Task:
    units: List[TaskUnit]
    extractor: Extractor

    def _run_task(self, unit: TaskUnit):
        extracted_results = self.extractor.run(unit)
        return extracted_results

    def run(self):
        return [self._run_task(task) for task in tasks]
