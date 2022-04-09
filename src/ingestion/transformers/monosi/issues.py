from ingestion.transformers.base import Transformer

class IssueTransformer(Transformer):
    @classmethod
    def message_formatter(cls, anomaly):
        return "Column {column_name} is alerting with a value of {value} on the metric {metric}.".format(
            column_name=anomaly['column_name'],
            value=anomaly['value'],
            metric=anomaly['metric'],
        )

    @classmethod
    def _transform(cls, anomalies):
        return [{
            'type': 'metric',
            'entity': "{}.{}.{}.{}".format(anomaly['database'], anomaly['schema'], anomaly['table_name'], anomaly['column_name']),
            'message': cls.message_formatter(anomaly),
            'value': anomaly['value'],
            'created_at': anomaly['time_window_end'],
        } for anomaly in anomalies]

    @classmethod
    def _original_schema(cls):
        return {
          "type": "array",
          "items": {
            "type": "object",
          },
          "minItems": 1
        }

    @classmethod
    def _normalized_schema(cls):
        return {
          "type": "array",
          "items": {
            "type": "object",
          },
          "minItems": 1
        }

