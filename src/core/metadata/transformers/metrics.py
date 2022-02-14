import logging
from core.models.metadata.metric import MsiMetric

# Takes db Results and converts to a SQLAlchemy object
class Transformer(object):
    @classmethod
    def _extract_window_from_row(cls, row):
        window_start = row.get('WINDOW_START') or row.get('window_start')
        window_end = row.get('WINDOW_END') or row.get('window_end')
        return window_start, window_end

    @classmethod
    def _extract_metric_and_col_from_alias(cls, alias):
        alias_parts = alias.split('__')
        if len(alias_parts) != 2:
            raise Exception("Could not parse alias name: {}".format(alias))
        return alias_parts[1], alias_parts[0]

    @classmethod
    def _filter_columns(cls, columns):
        filtered_values = ['window_start', 'window_end', 'row_count']
        for val in filtered_values:
            try:
                columns.remove(val)
            except:
                logging.warn('Could not filter column name: {}'.format(val))

        return columns

    @classmethod
    def run(cls, results, table_name):
        metrics = []

        rows = results['rows']
        columns = cls._filter_columns([column.name.lower() for column in results['columns']])

        for row in rows:
            time_window_start, time_window_end = cls._extract_window_from_row(row)
            interval_length_sec = None

            for column in columns:
                metric, column_name = cls._extract_metric_and_col_from_alias(column)
                value = row[column.upper()]

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
