---
id: getting-started
title: Getting Started
description: Data quality in minutes
sidebar_label: Getting Started
---


In order to use Monosi successfully, you will need to complete the following steps:

1. Deploy Monosi
2. Connect a data source
3. Create a data quality monitor
4. Connect an alerting destination


## 1. Deploy Monosi
1. Install Docker on your computer, and ensure that you have Docker Compose v2 installed.
2. Run the following commands

```
git clone https://github.com/monosidev/monosi.git
cd monosi
make compose-up
```
Navigate to http://localhost:3000 to access the web application once it has started.


## 2. Connect a Data Source

To add a data source, click “Add Data” on the Home screen.

<img src="/img/datasource/connect.png" height="700" alt="Connect Datasource" />

Then, click the button “Create Data Source” in order to enter the details for your data warehouse and connect. You can verify the connection after by clicking “Test”.

<img src="/img/datasource/create-1.png" height="700" alt="Create datasource 1" />
<img src="/img/datasource/create-2.png" height="700" alt="Create datasource 2" />

More detailed information about connecting to your specific data source and a list of supported integrations can be found <a href="/docs/integrations">here</a>.


## 3. Start Monitoring

Navigate to Monitors from the Home screen by clicking “Centralize & Monitor”.

<img src="/img/monitors/monitors.png" height="700" alt="Monitors" />

Then click the button “Create Monitor” and enter the details for the monitor that you would like to create. Once submitted Monosi will take a moment to get the historical data related to the data quality, and then begin regularly monitoring and alerting you of future issues.

<img src="/img/monitors/create.png" height="700" alt="Create monitor" />


## 4. Connect Alerts

Navigate to alerts by clicking “Add Alerts” on the Home screen.

<img src="/img/alerts/alerts.png" height="700" alt="Alerts" />

Then, click the button “Create Data Source” in order to enter the details for your alert destination and hit submit. 

<img src="/img/alerts/create.png" height="700" alt="Create alert" />

