from ingestion.transformers.base import JSONTransformer

class MonitorTransformer(JSONTransformer):
    @classmethod
    def _mapped_schema(cls):
        return '.rows | .[] | { "table_name": .NAME, "database": .DATABASE, "schema": .SCHEMA, "timestamp_field": .TIMESTAMP_FIELD, "type": "table_health" }'

    @classmethod
    def _original_schema(cls):
        return {
           "$schema":"http://json-schema.org/draft-04/schema#",
           "type":"object",
           "properties":{
              "rows":{
                 "type":"array",
                 "items":[
                    {
                       "type":"object",
                       "properties":{
                          "NAME":{
                             "type":"string"
                          },
                          "COL_NAME":{
                             "type":"string"
                          },
                          "COL_TYPE":{
                             "type":"string"
                          },
                          "COL_DESCRIPTION":{
                             "type":[
                                "string",
                                "null"
                             ]
                          },
                          "COL_SORT_ORDER":{
                             "type":[
                                "string",
                                "integer",
                                "null"
                             ]
                          },
                          "DATABASE":{
                             "type":"string"
                          },
                          "SCHEMA":{
                             "type":"string"
                          },
                          "DESCRIPTION":{
                             "type":[
                                "string",
                                "null"
                             ]
                          },
                          "IS_VIEW":{
                             "type":[
                                "string",
                                "null"
                             ]
                          }
                       },
                       "required":[
                          "NAME",
                          "COL_NAME",
                          "COL_TYPE",
                          "DATABASE",
                          "SCHEMA"
                       ]
                    }
                 ]
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


