import pytest
import sys
from mock import patch, MagicMock, mock_open

from bigpanda_splunk.configure import configure, write_shell_file, chown_bigpanda_files, verify_logging_permissions
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

    @patch("os.unlink")
    @patch("os.path.exists", return_value=True)
    def test_write_shell_file(self, exists_mock, unlink_mock):
        open_mock = mock_open()
        with patch("bigpanda_splunk.configure.open", open_mock, create=True):
            write_shell_file("/bla/runner")

        open_mock.assert_called_once_with("/opt/splunk/bin/scripts/bigpanda-splunk", "w")


    @patch("bigpanda_splunk.configure.validate_args", return_value=None)
    @patch("sys.exit")
    @patch("bigpanda_splunk.configure.write_shell_file")
    def test_configure_should_write_shell_wrapper_file(self, write_shell_file_mock, sys_exit_mock, validate_args_mock):
        write_shell_file_mock.side_effect = WTFException("AAA")
        configure("/bla/runner", ["", "token", "app_key"])
        write_shell_file_mock.assert_called_once_with("/bla/runner")

        sys_exit_mock.assert_called_once_with("BigPanda Splunk: Invalid permissions detected: AAA")

    @patch("bigpanda_splunk.configure.LOG")
    @patch("bigpanda_splunk.configure.setup_logging")
    def test_verify_logging_permissions(self, setup_logging_mock, log_mock):
        verify_logging_permissions()
        setup_logging_mock.assert_called_once()
        log_mock.info.assert_called_once_with("Testing permissions")

    @patch("bigpanda_splunk.configure.grp")
    @patch("bigpanda_splunk.configure.pwd")
    @patch("bigpanda_splunk.configure.glob")
    @patch("bigpanda_splunk.configure.os")
    def test_chown_bigpanda_files(self, os_mock, glob_mock, pwd_mock, grp_mock):
        grp_mock.getgrnam.return_value.gr_gid = "GIDz"
        pwd_mock.getpwnam.return_value.pw_uid = "UIDz"
        glob_mock.glob.return_value = ["f"]
        chown_bigpanda_files()
        os_mock.chown.assert_called_once_with("f", "UIDz", "GIDz")
