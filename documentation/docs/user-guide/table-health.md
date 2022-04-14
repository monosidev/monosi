---
id: table-health
title: Table Health Metrics
sidebar_label: Metrics
---

The Table Health monitor tracks various metrics (as listed below) on each column for a specified table and evaluates the results. It’s primary purpose is to ensure the data in the table specified is healthy and there are no anomalies.

<img src="/img/monitors/table_health.png" alt="Table health" />

## Supported Metrics

| Metric          | Description                                                                       | Column Type | String Representation |
| --------------- | --------------------------------------------------------------------------------- | ----------- | --------------------- |
| Count           | The number of rows for the field in a table                                       | Any         | count                 |
| Count Distinct  | The number of distinct rows for the field in a table                              | Any         | count_distinct        |
| Null            | The number of NULL values for a field in a table                                  | Any         | null                  |
| Max             | The maximum value of a field in a table                                           | Numeric     | max                   |
| Min             | The minimum value of a field in a table                                           | Numeric     | min                   |
| Mean            | The mean value of a field in a table                                              | Numeric     | mean                  |
| Std Dev         | The std dev value of a field in a table                                           | Numeric     | std_dev               |
| Is Zero         | The number of values that are zero of a field in a table                          | Numeric     | zero_rate             |
| Is Negative     | The number of values that are negative of a field in a table                      | Numeric     | negative_rate         |
| Mean Length     | The average length of the string                                                  | String      | mean_length           |
| Max Length      | The maximum length of the string                                                  | String      | max_length            |
| Min Length      | The minimum length of the string                                                  | String      | min_length            |
| Std Dev Length  | The std dev length of the string                                                  | String      | std_dev_length        |
| Integer Text    | The number of rows for a field which represent an integer value                   | String      | integer_rate          |
| Float Text      | The number of rows for a field which represent a float value                      | String      | float_rate            |
| Whitespace Text | The number of rows for a field which represent whitespace                         | String      | whitespace_rate       |
| Null/Empty Text | The number of rows for a field that are null or empty values                      | String      | null_rate             |
| Freshness       | The time difference between the current time and the last timestamp in the column | Timestamp   | freshness             |

## Anomaly Detection

The current implementation to detect anomalies involves calculating a Z-Score over the data set. If the value is outside of 3 standard deviations, it is considered an anomaly.

If an anomaly is detected by a monitor, the returned output contains information about the table, column, value, and metric that is anomalous. If none is found, then no errors are reported.
