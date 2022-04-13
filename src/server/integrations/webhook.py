import json
import logging
import requests
import sys


class WebhookIntegration:
    @classmethod
    def configuration_schema(cls):
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "title": "Webhook URL",
                },
            }
        }

    @classmethod
    def _modify_data(cls, data, metric):
        alert = {
            'message': 'Monosi - Anomaly Detected', 
            'type': 'table_health',
            'info': metric.to_dict()
        }

        data = data + alert

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

        data = []
        [cls._append_anomaly(data, anomaly) for anomaly in anomalies]
        data = json.dumps({'alerts': data})

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


