from dataclasses import dataclass
from typing import Any, List


@dataclass
class TaskUnit:
    request: Any

    def run(self, extractor):
        yield extractor.run(self)

@dataclass
class MultiTaskUnit(TaskUnit):
    request: Any

    def run(self, extractor):
        return extractor.run_multiple(self)

@dataclass
class Task:
    units: List[TaskUnit]
    extractor: Any

    def _run_unit(self, unit: TaskUnit):
        return unit.run(self.extractor)

    def run(self):
        for unit in self.units:
            yield self._run_unit(unit)
