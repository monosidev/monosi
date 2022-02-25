---
id: slack
title: Slack Integration
sidebar_label: Slack
---

Monosi integrates directly with Slack to be alert you in real-time of anomalies. It does so through the Incoming Webhooks feature of Slack.

1. Follow the steps over at Slack for creating an Incoming Webhook. Note that you may need permissions for your workspace in Slack to be able to create a webhook.
2. Add the webhook as a Slack integration in Monosi

Navigate to the Integrations page in Monosi, click the “Create Integration” button.

<img src="/img/integrations/overview.png" alt="Integrations home" />

Provide a name for this integration as well as the incoming webhook URL and hit submit.

<img src="/img/integrations/create.png" alt="Create integration" />

Once saved, anomalies will be sent to this Slack integration moving forward until deleted.
