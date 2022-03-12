from dataclasses import dataclass
from typing import List
import itertools

from .sources import Source

def flatten(arr):
	return list(itertools.chain.from_iterable(arr))

@dataclass
class Job:
	sources: List[Source]
	destinations: List[Destination]
	tasks: List[Task]

	def _create_source_tasks(source: Source):
		extractor = source.extractor()
		task_units = source.task_units()

		return [Task(extractor=extractor, unit=unit) for unit in units]

	def _create_tasks(self):
		self.tasks = flatten([self._create_source_tasks(source) for source in self.sources])

	def publish(self, data):
		return [destination.push(data) for destination in self.destinations]

	def run(self):
		# Create Tasks
		self._create_tasks()

		# Run tasks
		results = [task.run() for task in tasks]
		# Publish results
		[destination.push(data) for destination in self.destinations]
