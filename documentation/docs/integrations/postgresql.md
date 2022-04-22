---
id: postgresql
title: PostgreSQL Integration
sidebar_label: PostgreSQL
---

Monosi uses the [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) package to connect to PostgreSQL. In order to create a connection, the following data source form needs to be filled out.

<img src="/img/datasource/pg_connection.png" alt="PostgreSQL Form" width="850"/>

## Configuration Details

The following configuration details are necessary for a PostgreSQL connection.

| Key      | Description                                             | Required |
| -------- | ------------------------------------------------------- | -------- |
| user     | The username with which to connect monosi to PostgreSQL | Yes      |
| password | The password with which to connect monosi to PostgreSQL | Yes      |
| host     | The URL of the database host                            | Yes      |
| port     | The port of the database host                           | Yes      |
| database | The name of the database to connect to in PostgreSQL    | Yes      |
| schema   | The name of the schema to connect to in PostgreSQL      | Yes      |
