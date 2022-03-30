---
id: usage-data-preferences
title: Usage Data Preferences
sidebar_label: Usage Data Preferences
---

To help the team understand how people are interacting with monosi, we collect a few usage metrics. 

`database_connection_success` - helps us determine if a database connection was established successfully

`database_connection_fail` - helps us determine if there was an error with a database connection

`run_start` - helps us determine if a monitor run was started

`run_finish` - helps us determine if a monitor ran successfully

`scheduling_monitors` - helps us determine if a monitor was scheduled

You can opt out of this data collection at any point in time by setting the environment variable `SEND_ANONYMOUS_STATS` to false. 