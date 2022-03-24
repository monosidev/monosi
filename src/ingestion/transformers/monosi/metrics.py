from ingestion.transformers.base import JSONTransformer

class MetricTransformer(JSONTransformer):
    @classmethod
    def _mapped_schema(cls): # TODO: Add table, schema, database
        return '.[] | .[] | .[] | .rows | .[] | { "metric": (to_entries | .[] | select((.key | split("___") | .[1]) != null) | { "name": .key | split("___") | .[1], "column": .key | split("___") | .[0], "value": .value }), "time_window_start": .WINDOW_START, "time_window_end": .WINDOW_END, "table_name": .TABLE_NAME, "database": .DATABASE_NAME, "schema": .SCHEMA_NAME } | { "metric": .metric.name, "column_name": .metric.column, "value": .metric.value, "time_window_start": .time_window_start, "time_window_end": .time_window_end, "table_name": .table_name, "database": .database, "schema": .schema }'

    @classmethod
    def _original_schema(cls):
        # List of 
        return {
            "type": "object",
            "properties": {
                "bucket_start": { "type": "datetime" },
                "bucket_end": { "type": "datetime" },
                "row_count": { "type": "integer" },
                "database": { "type": "string" },
                "schema": { "type": "string" },
                "table": { "type": "string" },

                # A bunch of possible/optional metrics
            },
            "secret": [ ],
        }
        pass
        # raise NotImplementedError

    @classmethod
    def _normalized_schema(cls):
        return {
            "type": "object",
            "properties": {
                "table_name": { "type": "string" },
                "schema": { "type": "string" },
                "database": { "type": "string" },
                "column_name": { "type": "string" },
                "metric": { "type": "string" },
                "time_window_start": { "type": "datetime" },
                "time_window_end": { "type": "datetime" },
                "interval_length_sec": { "type": "integer" },
            },
            "secret": [ ],
        }

