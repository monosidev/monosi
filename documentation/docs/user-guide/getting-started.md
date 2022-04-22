---
id: getting-started
title: Getting Started
description: Data quality in minutes
sidebar_label: Getting Started
---


In order to use Monosi successfully, you will need to complete the following steps:

1. Deploy Monosi
2. Connect a data source
3. Connect an alerting destination
4. Track data quality monitors


## 1. Deploy Monosi

The fastest way to get up and running with Monosi is through Docker.

1. Install Docker on your computer, and ensure that you have Docker Compose v2 installed.
2. Run the following commands

```
git clone https://github.com/monosidev/monosi.git
cd monosi
make compose
```
Navigate to <a href="http://localhost:3000">http://localhost:3000</a> to access the web application once it has started.


## 2. Connect a Data Source

To add a data source, click “Add Data” on the Home screen.

<img src="/img/datasource/connect.png" height="700" alt="Connect Datasource" />

Then, click the button “Create Data Source” in order to enter the details for your data warehouse and connect. You can verify the connection after by clicking “Test”.

<img src="/img/datasource/create-1.png" height="700" alt="Create datasource 1" />
<img src="/img/datasource/create-2.png" height="700" alt="Create datasource 2" />

More detailed information about connecting to your specific data source and a list of supported integrations can be found <a href="/integrations">here</a>.

## 3. Connect Alerts

Navigate to alerts by clicking “Add Alerts” on the Home screen.

<img src="/img/alerts/alerts.png" height="700" alt="Alerts" />

Then, click the button “Create Data Source” in order to enter the details for your alert destination and hit submit. 

<img src="/img/alerts/create.png" height="700" alt="Create alert" />

## 4. Track data quality monitors

Navigate to Monitors from the Home screen by clicking “Centralize & Monitor”. If you don't see any monitors in the list, check the jobs page to ensure that a job has started. If there are no jobs running, wait a few minutes for Monosi to start (if there are no jobs after a few minutes, reach out in our [Slack](https://monosi.dev/slack))

<img src="/img/monitors/monitors.png" height="700" alt="Monitors" />

If you've previously connected a datasource, you should see a list of created monitors that Monosi has automatically profiled for you. Monosi analyzes the historical data related to the data quality of the detected tables and columns, then begins regularly monitoring and alerting you of future issues.

<img src="/img/monitors/monitors_index.png" height="700" alt="Monitor Index" />

When Monosi detects anomalies, it will send them to all connected alert destinations and surface them on the Issues page.

<img src="/img/issues/issues.png" height="700" alt="Issues" />

