import json
import logging
import requests
import sys


class SlackIntegration:
    @classmethod
    def configuration_schema(cls):
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "title": "Slack Webhook URL",
                },
            }
        }

    @classmethod
    def _modify_data(cls, data, metric):
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Monosi - Anomaly Detected",
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Type:*\nTable Health",
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Table:*\n{}.{}.{}".format(metric.database, metric.schema, metric.table_name)
                    },
                ],
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Column:*\n{}".format(metric.column_name),
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Metric:*\n{}".format(metric.metric),
                    }
                ]
            },
            # {
            #     "type": "section",
            #     "text": {
            #         "type": "mrkdwn",
            #         "text": " ",
            #     },
            #     "accessory": {
            #         "type": "button",
            #         "text": {
            #             "type": "plain_text",
            #             "text": "Learn More",
            #             "emoji": "true",
            #         },
            #         "url": "{}/monitors/{}/metrics?column_name={}&metric={}".format(request.base_url)
            #     }
            # }
        ]

        if len(data['blocks']) > 0:
            data['blocks'].append({"type": "divider"})
        data['blocks'] = data['blocks'] + blocks

        return data

    @classmethod
    def _retrieve_metric(cls, anomaly):
        metric_id = anomaly.get('metric_id')
        try:
            from server.middleware.db import db
            from server.models import Metric

            metric = db.session.query(Metric).filter(Metric.id == metric_id).one()
            return metric
        except:
            logging.error("Could not find metric with id: {}", metric_id)
            raise

    @classmethod
    def _append_anomaly(cls, data, anomaly):
        metric = cls._retrieve_metric(anomaly)
        cls._modify_data(data, metric)

        return data

    @classmethod
    def _create_headers(cls, data):
        byte_length = str(sys.getsizeof(data))
        headers = {'Content-Type': 'application/json', 'Content-Length': byte_length}

        return headers

    @classmethod
    def _create_request(cls, anomalies, config):
        url = config.get('url')
        if url is None:
            raise Exception("Slack Integration: Could not find a URL to send the message to.")

        data = {"text": "", "blocks": []}
        [cls._append_anomaly(data, anomaly) for anomaly in anomalies]
        data = json.dumps(data)

        headers = cls._create_headers(data)

        return url, data, headers

    @classmethod
    def send(cls, anomalies, config):
        if len(anomalies) == 0:
            return

        url, data, headers = cls._create_request(anomalies, config)

        try:
            response = requests.post(url, data=data, headers=headers)

            if response.status_code != 200:
                raise Exception(response.status_code, response.text)
        except Exception as e:
            logging.error("Request to Slack webhook URL {} failed.".format(url))
            raise e

