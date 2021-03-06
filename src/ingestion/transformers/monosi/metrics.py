from uuid import uuid4
from ingestion.transformers.base import JSONTransformer

class MetricTransformer(JSONTransformer):
    @classmethod
    def _mapped_schema(cls): # TODO: Add table, schema, database
        return '.rows | .[] | { "metric": (to_entries | .[] | select((.key | split("___") | .[1]) != null) | { "name": .key | split("___") | .[1], "column": .key | split("___") | .[0], "value": .value }), "time_window_start": .WINDOW_START, "time_window_end": .WINDOW_END, "table_name": .TABLE_NAME, "database": .DATABASE_NAME, "schema": .SCHEMA_NAME } | { "metric": .metric.name, "column_name": .metric.column, "value": .metric.value, "time_window_start": .time_window_start, "time_window_end": .time_window_end, "table_name": .table_name, "database": .database, "schema": .schema }'

    @classmethod
    def _original_schema(cls):
        return {
           "$schema":"http://json-schema.org/draft-04/schema#",
           "type":"object",
           "properties":{
              "rows":{
                 "type":"array",
                 "items": {
                   "type": "object"
                 },
                 "minItems": 1
              },
              "columns":{
                 "type":"array",
                 "items":{
                    "type":"string"
                 }
              }
           },
           "required":[
              "rows",
              "columns"
           ]
        }

    @classmethod
    def _normalized_schema(cls):
        return {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "table_name": {"type": "string"},
                    "schema": {"type": "string"},
                    "database": {"type": "string"},
                    "column_name": {"type": "string"},
                    "metric": {"type": "string"},
                    "value": {"type": "string"},
                    "time_window_start": {"type": "string"},
                    "time_window_end": {"type": "string"}
                },
                "required": ["id"]
            },
            "minItems": 1
        }


    @classmethod
    def _after_transform(cls, input):
        for metric in input:
            metric['id'] = uuid4().hex
        return input

