import abc
import json

from typing import Any, Dict, List


@dataclass
class SourceConfiguration:
	name: str
	configuration: str
	enabled: bool = True

	def __init__(self, configuration: Dict[str, Any]):
		self.configuration = configuration

	@classmethod
	def validate(cls, configuration):
		raise NotImplementedError

	def connection_string(self):
		raise NotImplementedError

	@abc.abstractproperty
	def type(self):
		raise NotImplementedError

	def to_dict(self):
		return {
			"name": self.name,
			"configuration": json.loads(self.configuration),
			"enabled": self.enabled,
			"type": self.type,
		}

class Source(object):
	"""docstring for Source"""
	def __init__(self, configuration: SourceConfiguration):
		super(Source, self).__init__()
		self.configuration = configuration

	def _before_pull(self):
		pass

	def _after_pull(self):
		pass

    @abc.abstractmethod
	def _pull(self):
		raise NotImplementedError

	def pull(self):
		self._before_pull()
		results = self._pull()
		self._after_pull()

		return results


class SQLAlchemyExtractor:
    def __init__(self, configuration):
        self.config = config
        self.driver = None

    def _initialize(self):
        try:
            from core.drivers.factory import load_driver
            driver_cls = load_driver(self.config)

            self.driver = driver_cls(self.config)
        except Exception as e:
            print(e)
            raise Exception("Could not initialize connection to database in Runner.")

    def _execute(self, sql: str):
        if self.driver is None:
            raise Exception("Initialize runner before execution.")

        results = self.driver.execute(sql)
        return results

    def run(self, unit: str):
        self._initialize()
        sql = unit.request

        return self._execute(sql)

class SQLAlchemySourceDialect:
    @classmethod
    def _approx_distinct_count(cls):
        return "COUNT(DISTINCT {})"
    
    @classmethod
    def _approx_distinctness(cls):
        return "{} / CAST(COUNT(*) AS NUMERIC)".format(cls.approx_distinct_count())

    @classmethod
    def _numeric_mean(cls):
        return "AVG({})"

    @classmethod
    def _numeric_min(cls):
        return "MIN({})"

    @classmethod
    def _numeric_max(cls):
        return "MAX({})"

    @classmethod
    def _numeric_std(cls):
        return "STDDEV(CAST({} as double))"

    @classmethod
    def _mean_length(cls):
        return cls.numeric_mean().format("LENGTH({})")

    @classmethod
    def _max_length(cls):
        return cls.numeric_max().format("LENGTH({})")

    @classmethod
    def _min_length(cls):
        return cls.numeric_min().format("LENGTH({})")

    @classmethod
    def _std_length(cls):
        return cls.numeric_std().format("LENGTH({})")

    @classmethod
    def _text_int_rate(cls):
    	raise NotImplementedError

    @classmethod
    def _text_number_rate(cls):
    	raise NotImplementedError

    @classmethod
    def _text_uuid_rate(cls):
    	raise NotImplementedError

    @classmethod
    def text_all_spaces_rate(cls):
    	raise NotImplementedError

    @classmethod
    def _text_null_keyword_rate(cls):
    	raise NotImplementedError

    @classmethod
    def _zero_rate(cls):
    	raise NotImplementedError

    @classmethod
    def _negative_rate(cls):
    	raise NotImplementedError

    @classmethod
    def _completeness(cls):
    	raise NotImplementedError

    @classmethod
    def schema_query(cls):
    	raise NotImplementedError

    @classmethod
    def table_metrics_query(cls):
    	raise NotImplementedError

    @classmethod
    def query_access_logs_query(cls):
    	raise NotImplementedError
    	
    @classmethod
    def query_copy_logs_query(cls):
    	raise NotImplementedError


@dataclass
class SQLAlchemySource(Source):
	dialect: SQLAlchemySourceDialect

	def _schema(self) -> TaskUnit:
		return TaskUnit(request=self.dialect.schema_query())

	def _metrics(self) -> List[TaskUnit]:
		tables = []
		return [TaskUnit(request=self.dialect.table_metrics_query(table)) for table in tables]

	def _query_access_logs(self) -> TaskUnit:
		return TaskUnit(request=self.dialect.query_access_logs_query())

	def _query_copy_logs(self) -> TaskUnit:
		return TaskUnit(request=self.dialect.query_copy_logs_query())

	def task_units(self) -> List[TaskUnit]:
		units = [
			self._schema(),
			self._query_access_logs(),
			self._query_copy_logs()
		]
		[units.append(unit) for unit in self._metrics()]

		return units

	def tasks(self):
		extractor = SQLAlchemyExtractor(self.configuration)
		units = self.task_units()

		return [Task(extractor=extractor, units=unit) for unit in units]
