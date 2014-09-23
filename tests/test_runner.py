import pytest
import sys
from mock import patch, MagicMock, mock_open

from bigpanda_splunk.runner import alert
from tests import WTFException



class TestRunner(object):
    @patch("bigpanda_splunk.runner.time")
    @patch("bigpanda_splunk.runner.setup_logging")
    @patch("bigpanda_splunk.runner.send_alert")
    @patch("bigpanda_splunk.runner.read_config", return_value={
        "app_key": "123"
        })
    def test_alert_should_populate_json(self, read_config_mock, send_alert_mock, setup_logging_mock, time_mock):
        expected_timestamp = 1411388217
        time_mock.time.return_value = expected_timestamp
        alert(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"])
        read_config_mock.assert_called_once()
        setup_logging_mock.assert_called_once()
        send_alert_mock.assert_called_once_with({
            "app_key": "123",
            "status": "critical",
            "number_of_events": "two",
            "primary_property": "report_name",
            "secondary_property": "trigger",
            "search_terms": "three",
            "query_string": "four",
            "report_name": "five",
            "trigger": "six",
            "link": "seven",
            "results_file": "nine",
            "timestamp": expected_timestamp,
            "incident_identifier": 'five_' + str(expected_timestamp)
        }, {"app_key": "123"})
