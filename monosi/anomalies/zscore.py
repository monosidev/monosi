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

    @classmethod
    def anomalies(cls, values: List[float], sensitivity: float = 3.0):
        z_scores = cls.run(values)

        anomaly_scores = []
        for z_score in z_scores:
            if abs(z_score) > sensitivity:
                anomaly_scores.append(z_score)

        return anomaly_scores

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