import abc

class Dialect:
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'approx_distinct_count') and 
                callable(subclass.approx_distinct_count) and 
                NotImplemented)

    @abc.abstractclassmethod
    def approx_distinct_count(cls):
        raise NotImplementedError

class GenericDialect(Dialect):
    @classmethod
    def approx_distinct_count(cls):
        return "COUNT(DISTINCT {})"
    
    @classmethod
    def approx_distinctness(cls):
        return "{} / CAST(COUNT(*) AS NUMERIC)".format(cls.approx_distinct_count())

    @classmethod
    def numeric_mean(cls):
        return "AVG({})"

    @classmethod
    def numeric_min(cls):
        return "MIN({})"

    @classmethod
    def numeric_max(cls):
        return "MAX({})"

    @classmethod
    def numeric_std(cls):
        return "STDDEV(CAST({} as double))"

    @classmethod
    def mean_length(cls):
        return cls.numeric_mean().format("LENGTH({})")

    @classmethod
    def max_length(cls):
        return cls.numeric_max().format("LENGTH({})")

    @classmethod
    def min_length(cls):
        return cls.numeric_min().format("LENGTH({})")

    @classmethod
    def std_length(cls):
        return cls.numeric_std().format("LENGTH({})")
