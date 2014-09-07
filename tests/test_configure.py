import pytest
import sys
from mock import patch, MagicMock, mock_open

from bigpanda_splunk.configure import configure
from tests import WTFException



class TestConfigure(object):
    @patch("sys.exit")
    def test_configure_should_validate_input(self, sys_exit_mock):
        configure("/bla/runner.bla", [""])

        sys_exit_mock.assert_called_once_with("BigPanda Splunk\nUsage: runner.bla TOKEN APP_KEY")

    @patch("sys.exit")
    def test_configure_should_validate_splunk_home(self, sys_exit_mock):
        configure("/bla/runner", ["", "token", "app_key"])

        sys_exit_mock.assert_called_once_with("BigPanda Splunk: Splunk installation not found!")

    @patch("bigpanda_splunk.configure.write_config")
    @patch("os.unlink")
    @patch("sys.exit")
    @patch("os.path.exists", return_value=True)
    def test_configure_should_write_shell_wrapper_file(self, exists_mock, sys_exit_mock, unlink_mock, write_config_mock):
        open_mock = mock_open()
        write_config_mock.side_effect = WTFException
        with patch("bigpanda_splunk.configure.open", open_mock, create=True):
            configure("/bla/runner", ["", "token", "app_key"])
        print "Call Args?", write_config_mock.call_args
        open_mock.assert_called_once_with("/opt/splunk/bin/scripts/bigpanda-splunk", "w")
