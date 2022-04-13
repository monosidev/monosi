---
id: bigquery
title: BigQuery Integration
sidebar_label: BigQuery
---

Monosi supports BigQuery data warehouse connections. Currently, only authentication through a `service_account.json` file is supported. If you do not have a service account, please follow the instructions to create one [here](https://cloud.google.com/docs/authentication/getting-started).

If you require other forms of authentication, please [open an issue](https://github.com/monosidev/monosi/issues/new?assignees=&labels=&template=feature_request.md).

<img src="/img/integrations/bigquery_connection.png" alt="BigQuery Integration" />

## Configuration Details

| Key             | Description                                              | Required |
| --------------- | -------------------------------------------------------- | -------- |
| project         | The name of the BigQuery project you want to connect     | Yes      |
| dataset         | The name of the dataset you want to connect              | Yes      |
| service_account | The `service_account.json` file associated with your IAM | Yes      |

