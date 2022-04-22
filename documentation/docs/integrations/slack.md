---
id: slack
title: Slack Integration
sidebar_label: Slack
---

Monosi integrates directly with Slack to be alert you in real-time of anomalies. It does so through the Incoming Webhooks feature of Slack.

1. Follow the steps over at Slack for creating an [Incoming Webhook](https://api.slack.com/messaging/webhooks). Note that you may need permissions for your workspace in Slack to be able to create a webhook.
2. Add the webhook as a Slack integration in Monosi

Navigate to the Integrations page in Monosi, click the “Create Integration” button.

<img src="/img/integrations/overview.png" alt="Integrations home" />

Provide a name for this integration as well as the incoming webhook URL and hit submit.

<img src="/img/integrations/slack_create.png" alt="Create integration" />

Once saved, anomalies will be sent to this Slack integration moving forward until deleted. 

The format of the Slack message is shown below. It includes the monitor type, the database table that the anomaly was detected in, the column of the tabel that the anomaly was detected in, and the health metric that failed. 

<img src="/img/slack_alert.svg" alt="Slack alert" />
