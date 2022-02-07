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

    def _monitor_header(self, monitor):
        header = ""
        if monitor['type'] == 'table':
            header += "\nTable Health: {}".format(monitor.get('name') or monitor.get('table'))
        elif monitor['type'] == 'custom':
            header += "\nCustom Monitor: {}".format(monitor.get('name') or monitor.get('sql'))
        elif monitor['type'] == 'schema':
            header += "\nSchema Monitor: {}".format(monitor.get('name') or monitor.get('table'))

        if monitor.get('description'):
            header += "\nDescription: {}".format(monitor.get('description'))

        return header

    def dump_monitor(self, monitor):
        monitor_dict = monitor['monitor']

        msg = ""
        msg += self._monitor_header(monitor_dict)

        if len(monitor['failed_metrics']) > 0:
            for metric in monitor['failed_metrics']:
                msg += "\n"
                msg += metric['message']
        else:
            msg += "\nNo Failures."

        msg += "\n\nStart: {}\tStop: {}\n\n".format(monitor['start_time'], monitor['stop_time'])
        return msg

    def dump_summary(self, summary):
        monitors = summary['monitors']

        message = ""
        for monitor in monitors:
            message += self.dump_monitor(monitor)
            message += "\n"

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

