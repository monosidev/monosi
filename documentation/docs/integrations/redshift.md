---
id: redshift
title: Redshift Integration
sidebar_label: Redshift
---

Monosi uses the [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) package (along with the Redshift adapter) to connect to Redshift. In order to create a connection, the following data source form needs to be filled out.

<img src="/img/datasource/redshift_connection.png" alt="Redshift Form" width="850"/>

## Configuration Details

The following configuration details are necessary for a Redshift connection. The configuration details are the same as the PostgreSQL source.

| Key      | Description                                           | Required |
| -------- | ----------------------------------------------------- | -------- |
| user     | The username with which to connect monosi to Redshift | Yes      |
| password | The password with which to connect monosi to Redshift | Yes      |
| host     | The URL of the database host                          | Yes      |
| port     | The port of the database host                         | Yes      |
| database | The name of the database to connect to in Redshift    | Yes      |
| schema   | The name of the schema to connect to in Redshift      | Yes      |
