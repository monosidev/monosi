import requests
import sys
import json

from server.integrations.base import IntegrationDefinition

class SlackIntegration(IntegrationDefinition):
    @classmethod
    def configuration_schema(cls):
        return {
            "type": "object",
            "properties": {
                "url": {"type": "string", "title": "Slack Webhook URL"},
            },
            "secret": [ "url" ],
        }

    @staticmethod
    def _create_request_data(message):
        body = {
            "text": message
        }
        byte_length = str(sys.getsizeof(body))
        headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
        return headers, json.dumps(body)

    def write(self, message, color=None):
        url = json.loads(self.configuration)['url']
        headers, data = self._create_request_data(message)

        try:
            response = requests.post(url, data=data, headers=headers)

            if response.status_code != 200:
                raise Exception(response.status_code, response.text)
        except Exception as e:
            print(e)
            raise Exception("Request to Slack webhook URL {} failed.".format(url))

    def dump_failures(self, failed_tests):
        pass
        # if len(failed_tests) > 0:
        #     message = ""
        #     message += "\nFailures\n"

        #     for failed_test in failed_tests:
        #         message += "\tAnomalies: {}\n".format(len(failed_test.anomalies()))
        #         message += "\n"

        #     self.write(message)

    def dump_summary(self, summary):
        monitor = summary['monitor']

        message = ""
        message += "Monitor: {monitor_name}".format(monitor_name=monitor.name)
        if monitor.description:
            message += "\nDescription: {monitor_description}".format(monitor_description=monitor.description)
        message += "\nTotal Time: {} seconds, SQL Load Time: {} seconds".format(summary['total_time'], summary['load_time'])
        message += "\n"
        
        message += "\nTotal Metrics: {}".format(summary['test_count'])
        message += "\nFailed Metrics: {}".format(summary['failed_count'])
        message += "\n\nAnomaly details coming soon to slack integration."
        self.write(message)

    def dump_pending(self, none_obj):
        pass

    def close(self, none_obj):
        pass

    def monitor_started(self, none_obj):
        pass

    def monitor_finished(self, none_obj):
        pass

    def message(self, none_obj):
        pass

    def stop(self, none_obj):
        pass

    def dump_skipped(self, skipped_tests):
        pass

    def test_started(self, none_obj):
        pass

    def test_finished(self, none_obj):
        pass

    def test_passed(self, none_obj):
        pass
        
    def test_pending(self, none_obj):
        pass

    def test_failed(self, none_obj):
        pass

    def start_dump(self, none_obj):
        # self.write('start_dump', Color.ENDC)
        pass

