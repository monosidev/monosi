from ingestion.transformers.base import Transformer#, JSONTransformer

# class MonitorTransformer(JSONTransformer):
    # @classmethod
    # def _mapped_schema(cls):
    #     return '.rows | .[] | { "table_name": .NAME, "database": .DATABASE, "schema": .SCHEMA, "timestamp_field": .TIMESTAMP_FIELD, "type": "table_health" }'

class MonitorTransformer(Transformer):
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
        }

    @classmethod
    def _fqtn_info(cls, item):
        return item['DATABASE'], item['SCHEMA'], item['NAME']

    @classmethod
    def _col_info(cls, item):
        return item['COL_NAME'], item['COL_TYPE']

    @classmethod
    def _parse_timestamps(cls, item, timestamp_fields):
        fqtn_info = cls._fqtn_info(item)
        col_name, col_type = cls._col_info(item)

        if fqtn_info not in timestamp_fields:
            timestamp_fields[fqtn_info] = []

        if 'date' in col_type or "timestamp" in col_type:
            timestamp_fields[fqtn_info].append(col_name)

    @classmethod
    def _timestamp_field(cls, cols): # TODO: Improve
        if len(cols) == 0:
            return None

        return cols[0]

    @classmethod
    def _transform(cls, input):
        monitors = []

        table_timestamps = {}
        [cls._parse_timestamps(item, table_timestamps) for item in input['rows']]

        for fqtn, timestamp_cols in table_timestamps.items():
            monitors.append({
                'table_name': fqtn[2],
                'database': fqtn[0],
                'schema': fqtn[1],
                'timestamp_field': cls._timestamp_field(timestamp_cols), # What do
                'type': 'table_health',
            })

        return monitors
