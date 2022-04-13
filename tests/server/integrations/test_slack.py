import pytest

import server.integrations.slack as slack

@pytest.fixture
def anomalies():
    return []

@pytest.fixture
def config():
    return {'url': 'http://localhost:3000/notarealurl'}

@pytest.fixture
def empty_data():
    return { "text": "", "blocks": [] }

@pytest.fixture
def data(empty_data):
    empty_data['blocks'] = [
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
                        "text": "*Table:*\n{}.{}.{}".format("database", "schema", "table_name")
                    },
                ],
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Column:*\n{}".format("column_name"),
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Metric:*\n{}".format("metric"),
                    }
                ]
            },
        ]
    return empty_data

def test__create_headers_empty(empty_data):
    headers = slack.SlackIntegration._create_headers(empty_data)

    assert 'Content-Type' in headers
    assert 'Content-Length' in headers
    
    assert headers['Content-Type'] == 'application/json'
    assert int(headers['Content-Length']) == 232

def test__create_headers_not_empty(data):
    headers = slack.SlackIntegration._create_headers(data)

    assert 'Content-Type' in headers
    assert 'Content-Length' in headers
    
    assert headers['Content-Type'] == 'application/json'
    assert int(headers['Content-Length']) == 232
 
 # TODO: Requires DB setup for a metric to retrieve

# def test__retrieve_metric(anomalies):
#     anomaly = anomalies[0]
#     metric = slack.SlackIntegration._retrieve_metric(anomaly)

# def test__append_anomaly(data, anomalies):
#     anomaly = anomalies[0]
#     slack.SlackIntegration._append_anomaly(data, anomaly)

# def test__create_request(anomalies, config):
#     url, data, headers = slack.SlackIntegration._create_request(anomalies, config)

def test__send_empty(config): 
    empty_anomalies = []
    slack.SlackIntegration.send(empty_anomalies, config)


# def test__send(): # TODO: Intercept request
#     raise NotImplementedError

