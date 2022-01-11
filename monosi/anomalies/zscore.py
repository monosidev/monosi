@dataclass
class Anomaly:
    point: MetricDataPoint
    expected_range_start: float
    expected_range_end: float

class ZScoreAlgorithm:
    @classmethod
    def _mean(cls, values: List[float]):
        return round(sum(values) / len(values), 2)

    @classmethod
    def _std_dev(cls, values: List[float]):
        values_mean = cls._mean(values)

        distances = [((value - values_mean) ** 2) for value in values]
        distances_mean = cls._mean(distances)
        std_dev = round(sqrt(distances_mean), 2)

        return std_dev

    def anomalies(cls, data: List['MetricDataPoint'], sensitivity: float = 3.0):
        values = [point.value for point in data]

        try:
            mean = cls._mean(values)
            std_dev = cls._std_dev(values)
        except ZeroDivisionError:
            return []

        if (std_dev == 0): return []

        anomalies = []
        for point in data:
            try:
                z_score = round(((point.value - mean) / std_dev), 2)

                expected_range_start = point.value + std_dev * sensitivity
                expected_range_stop = point.value - std_dev * sensitivity

                if abs(z_score) > sensitivity:
                    anomaly = Anomaly(
                        point=point, 
                        expected_range_start=expected_range_start, 
                        expected_range_stop=expected_range_stop
                    )
                    anomalies.append(anomaly)

            except TypeError:
                return []

        return anomalies


    @classmethod
    def run(cls, values: List[float]):
        try:
            mean = cls._mean(values)
            std_dev = cls._std_dev(values)
        except ZeroDivisionError:
            return []

        if (std_dev == 0): return []

        z_scores = []
        for value in values:
            try:
                z_score = round(((value - mean) / std_dev), 2) 
                z_scores.append(z_score)
            except TypeError:
                return []

        return z_scores