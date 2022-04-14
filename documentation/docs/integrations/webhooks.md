---
id: webhooks
title: Webhooks Integration
sidebar_label: Webhooks
---

Monosi supports sending alerts to custom endpoints through webhooks.

1. Navigate to the Integrations subpage in Settings
2. Click on the Create Integration button and select the Webhook integration in the drawer
3. Provide a name for this integration as well as the incoming webhook URL and hit submit.

<img src="/img/integrations/webhook_alert.png" alt="Webhook Alert" />

Once saved, anomalies will be sent to this Webhook integration moving forward until deleted.

The payload format of the Webhook is detailed below:

```
{
    alerts: [
        {
            message: 'Monosi - Anomaly Detected', 
            type: 'table_health',
            info: {
                table_name: ""
                schema: ""
                database: ""
                column_name: ""
                metric: ""
                value: ""
                time_window_start: ""
                time_window_end: ""
                interval_length_sec: ""
                id: ""
                created_at: ""
            }
        }
        ...
    ]
}
```
