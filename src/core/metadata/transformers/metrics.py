from core.models.metadata.metric import MsiMetric

# Takes db Results and converts to a SQLAlchemy object
class Transformer(object):
    @classmethod
    def _extract_window_from_row(cls, row):
        return None, None

    @classmethod
    def _extract_metric_and_col_from_alias(cls, row):
        return None, None

    @classmethod
    def _filter_columns(cls, columns):
        filtered_values = ['time_window_start', 'time_window_end', 'row_count']
        [columns.remove(val) for val in filtered_values]

        return columns

    @classmethod
    def run(cls, results, table_name)
        metrics = []

        rows = results['rows']
        columns = cls._filter_columns([column.name.lower() for colum in results['columns']])

        for row in rows:
            time_window_start, time_window_end = cls._extract_window_from_row(row)
            interval_length_sec = None

            for column in columns:
                metric, column_name = cls._extract_metric_and_col_from_alias(column)
                value = row[column]

                metric = MsiMetric(
                    table_name=table_name,
                    column_name=column_name,
                    metric=metric,
                    value=value,
                    time_window_start=time_window_start,
                    time_window_end=time_window_end,
                    interval_length_sec=interval_length_sec,
                )
                metrics.append(metric)

        return metrics
