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
    def _create_request_data(cls, metric):
        body = {
            "text": "Danny Torrence left a 1 star review for your property.",
            "blocks": [
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
        }
        byte_length = str(sys.getsizeof(body))
        headers = {'Content-Type': 'application/json', 'Content-Length': byte_length}

        return headers, json.dumps(body)

    @classmethod
    def _retrieve_metric(cls, metric_id):
        from server.middleware.db import db
        from server.models import Metric

        metric = db.session.query(Metric).filter(Metric.id == metric_id).one()
        return metric

    @classmethod
    def send(cls, metric_id, config):
        try:
            metric = cls._retrieve_metric(metric_id)

            url = config['url']
            headers, data = cls._create_request_data(metric)
        except Exception as e:
            logging.error("Could not find metric with id: {}", metric_id)
            return
        
        try:
            response = requests.post(url, data=data, headers=headers)
            
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)
        except Exception as e:
            logging.error("Request to Slack webhook URL {} failed.".format(url))
            raise e

