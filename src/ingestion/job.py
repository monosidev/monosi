from dataclasses import dataclass
from typing import List
import itertools

from .destinations import Destination
from .sources import Source
from .task import Task


def flatten(arr):
	return list(itertools.chain.from_iterable(arr))

@dataclass
class Job:
	sources: List[Source]
	destinations: List[Destination]
	tasks: List[Task]

	def _create_source_tasks(self, source: Source):
		extractor = source.extractor()
		task_units = source.task_units()

		return [Task(extractor=extractor, units=[unit]) for unit in task_units]

	def _create_tasks(self):
		self.tasks = flatten([self._create_source_tasks(source) for source in self.sources])

	def publish(self, data):
		return [destination.push(data) for destination in self.destinations]

	def run(self):
		# Create Tasks
		self._create_tasks()

		# Run tasks
		results = [task.run() for task in self.tasks]
		# Publish results
		[destination.push(results) for destination in self.destinations]
