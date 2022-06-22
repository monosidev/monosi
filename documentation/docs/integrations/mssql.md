---
id: mssql
title: Micsoft SQL Server Integration
sidebar_label: MSSQL
---

## Configuration Details

The configuration details are the same as the PostgreSQL source

| Key       | Description                                             | Required |
|-----------|---------------------------------------------------------|----------|
| user      | The username with which to connect monosi to Redshift  | Yes      |
| password  | The password with which to connect monosi to Redshift  | Yes      |
| host      | The URL of the database host                             | Yes      |
| database  | The name of the database to connect to in Redshift     | Yes      |
| schema    | The name of the schema to connect to in Redshift       | Yes      |

NOTE: Support for the Microsoft SQL Server database via the pymssql driver. Further information on this driver can be found here: https://github.com/pymssql/pymssql 