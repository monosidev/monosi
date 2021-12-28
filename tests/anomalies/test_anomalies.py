from monosi.anomalies import ZScoreAnomalyDetector
from monosi.monitors.table_metrics import MetricStat
import unittest


class ZScoreAnomalyDetectorTestSuite(unittest.TestCase):
    """Anomaly detector test cases."""

    def test_mean_calculation(self):
        values = [1,2,3,4,5]
        mean = ZScoreAnomalyDetector._mean(values)
        assert mean == 3

    def test_std_dev_calculation(self):
        values = [1,2,3,4,5]
        std_dev = ZScoreAnomalyDetector._std_dev(values)
        assert std_dev == 1.41

    def test_z_scores_calculation(self):
        stat_1 = MetricStat(
            table="EXAMPLE_TABLE_1",
            column="EXAMPLE_COLUMN_1",
            metric="EXAMPLE_COLUMN_1",
            window_start="WINDOW_START",
            window_end="WINDOW_END",
            value=0.0,
        )
        stat_2 = MetricStat(
            table="EXAMPLE_TABLE_2",
            column="EXAMPLE_COLUMN_2",
            metric="EXAMPLE_COLUMN_2",
            window_start="WINDOW_START",
            window_end="WINDOW_END",
            value=10.0,
        )
        stat_3 = MetricStat(
            table="EXAMPLE_TABLE_3",
            column="EXAMPLE_COLUMN_3",
            metric="EXAMPLE_COLUMN_3",
            window_start="WINDOW_START",
            window_end="WINDOW_END",
            value=100.0,
        )
        stats = [stat_1, stat_2, stat_3]
        resulting_stats = ZScoreAnomalyDetector._z_scores(stats)
        assert len(resulting_stats) == 3
        assert resulting_stats[0].std_dev == 44.97
        assert resulting_stats[0].z_score == -0.82

    def test_z_scores_calculation_with_none(self):
        stat_1 = MetricStat(
            table="EXAMPLE_TABLE_1",
            column="EXAMPLE_COLUMN_1",
            metric="EXAMPLE_COLUMN_1",
            window_start="WINDOW_START",
            window_end="WINDOW_END",
            value=None,
        )
        stats = [stat_1]
        resulting_stats = ZScoreAnomalyDetector._z_scores(stats)
        assert len(resulting_stats) == 0

    def test_z_scores_calculation_with_some_none(self):
        stat_1 = MetricStat(
            table="EXAMPLE_TABLE_1",
            column="EXAMPLE_COLUMN_1",
            metric="EXAMPLE_COLUMN_1",
            window_start="WINDOW_START",
            window_end="WINDOW_END",
            value=None,
        )
        stat_2 = MetricStat(
            table="EXAMPLE_TABLE_2",
            column="EXAMPLE_COLUMN_2",
            metric="EXAMPLE_COLUMN_2",
            window_start="WINDOW_START",
            window_end="WINDOW_END",
            value=10.0,
        )
        stat_3 = MetricStat(
            table="EXAMPLE_TABLE_3",
            column="EXAMPLE_COLUMN_3",
            metric="EXAMPLE_COLUMN_3",
            window_start="WINDOW_START",
            window_end="WINDOW_END",
            value=100.0,
        )
        stat_4 = MetricStat(
            table="EXAMPLE_TABLE_3",
            column="EXAMPLE_COLUMN_3",
            metric="EXAMPLE_COLUMN_3",
            window_start="WINDOW_START",
            window_end="WINDOW_END",
            value=None,
        )
        stats = [stat_1, stat_2, stat_3, stat_4]
        resulting_stats = ZScoreAnomalyDetector._z_scores(stats)
        assert len(resulting_stats) == 2
        assert resulting_stats[0].std_dev == 45.0
        assert resulting_stats[0].z_score == -1.0


if __name__ == '__main__':
    unittest.main()
