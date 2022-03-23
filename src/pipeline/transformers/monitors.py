from .base import JSONTransformer

class MonitorTransformer(JSONTransformer):
    @classmethod
    def _mapped_schema(cls): # TODO: Add table, schema, database
        return '.[] | .[] | .[] | .rows | .[] | { "table_name": .table_name, "database": .database, "schema": .schema, "timestamp_field": .timestamp_field, "type": "table_health" }'

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


