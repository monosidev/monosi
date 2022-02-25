---
id: snowflake
title: Snowflake Integration
sidebar_label: Snowflake
---

## Configuration Details

| Key       | Description                                             | Required |
|-----------|---------------------------------------------------------|----------|
| user      | The username with which to connect monosi to snowflake  | Yes      |
| password  | The password with which to connect monosi to snowflake  | Yes      |
| account   | The snowflake account name (typically found in the URL) | Yes      |
| warehouse | The name of the warehouse to connect to in Snowflake    | Yes      |
| database  | The name of the database to connect to in Snowflake     | Yes      |
| schema    | The name of the schema to connect to in Snowflake       | Yes      |

## Permissions (Optional)

Best practice is to create a specific user account with the permissions that monosi needs to be able to monitor the quality of your data. This ensures that Monosi has the permissions necessary to operate on the snowflake data warehouse and that your information is secure.

In order to connect to Snowflake, create a MONOSI user account with the following permissions:
```
# Create role
CREATE ROLE MONOSI_ROLE;
GRANT ROLE MONOSI_ROLE TO ROLE SYSADMIN;

# Grant warehouse permissions
GRANT USAGE ON WAREHOUSE <YOUR_WAREHOUSE> TO ROLE MONOSI_ROLE;
GRANT OPERATE ON WAREHOUSE <YOUR_WAREHOUSE> TO ROLE MONOSI_ROLE;
GRANT MONITOR ON WAREHOUSE <YOUR_WAREHOUSE> TO ROLE MONOSI_ROLE;

# Create user
CREATE USER MONOSI WITH DEFAULT_ROLE = MONOSI_ROLE DEFAULT_WAREHOUSE = <YOUR_WAREHOUSE> PASSWORD = '<password used in monosi config.yml>';
GRANT ROLE MONOSI_ROLE TO USER MONOSI;
```

Alternatively, you can also grant specific permissions to the MONOSI_ROLE by running the following for each of the database/schemas you would like to provide access to monosi:
```
GRANT USAGE ON DATABASE "<database>" TO ROLE MONOSI_ROLE;
GRANT USAGE ON SCHEMA "<database>"."<schema>" TO ROLE MONOSI_ROLE;
GRANT SELECT ON ALL TABLES IN SCHEMA "<database>"."<schema>" TO ROLE MONOSI_ROLE;
GRANT SELECT ON FUTURE TABLES IN SCHEMA "<database>"."<schema>" TO ROLE MONOSI_ROLE;
GRANT SELECT ON ALL VIEWS IN SCHEMA "<database>"."<schema>" TO ROLE MONOSI_ROLE;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA "<database>"."<schema>" TO ROLE MONOSI_ROLE;
GRANT USAGE ON ALL FUNCTIONS IN SCHEMA "<database>"."<schema>" TO ROLE MONOSI_ROLE;
GRANT USAGE ON FUTURE FUNCTIONS IN SCHEMA "<database>"."<schema>" TO ROLE MONOSI_ROLE
```
Now that you've created this account, you can use the username, password, warehouse, and database details from above in the source configuration details.
