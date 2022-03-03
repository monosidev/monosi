---
id: sources
title: Sources
sidebar_label: Sources
tags:
  - msi
---

# Sources


## Metrics

| Field               | Type | Required |
|---------------------|------|----------|
| id                  |      |          |
| table_name          |      |          |
| schema              |      |          |
| database            |      |          |
| column_name         |      |          |
| metric              |      |          |
| value               |      |          |
| time_window_start   |      |          |
| time_window_end     |      |          |
| interval_length_sec |      |          |

## Schema

### Table
```
SELECT 
  TABLE_CATALOG, 
  TABLE_SCHEMA,
  TABLE_NAME, 
  TABLE_OWNER, 
  TABLE_TYPE, 
  IS_TRANSIENT, 
  RETENTION_TIME, 
  AUTO_CLUSTERING_ON, 
  COMMENT 
FROM "ANALYTICS".information_schema.tables 
WHERE 
  table_schema NOT IN ('INFORMATION_SCHEMA') 
  AND TABLE_TYPE NOT IN ('VIEW', 'EXTERNAL TABLE') 
ORDER BY TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME;
```

### Column
```
SELECT 
  '"' || TABLE_CATALOG || '"."' || TABLE_SCHEMA || '"."' || TABLE_NAME || '"' AS FULL_NAME, 
  COLUMN_NAME, 
  DATA_TYPE, 
  COLUMN_DEFAULT, 
  IS_NULLABLE, 
  COMMENT, 
  CHARACTER_MAXIMUM_LENGTH, 
  NUMERIC_PRECISION, 
  NUMERIC_SCALE, 
  DATETIME_PRECISION 
FROM "ANALYTICS".information_schema.columns;
```

## Logs

### Query History

### Copy History


