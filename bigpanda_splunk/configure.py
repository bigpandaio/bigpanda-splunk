from bigpanda_splunk import \
        SPLUNK_HOME, \
        SCRIPT_NAME, \
        LOG, write_config, setup_logging, get_path
from bigpanda_splunk.runner import send_test_alert

import os
import sys

def configure(runner_path):
    """
    Configure BigPanda Splunk Provider
    """
    token, app_key = sys.argv[1], sys.argv[2]
    if not os.path.exists(SPLUNK_HOME):
        sys.exit("BigPanda Splunk: Splunk installation not found!")

    try:
        os.symlink(
            os.path.join(runner_path, SCRIPT_NAME), get_path(SCRIPT_NAME))
        write_config(token, app_key)
        setup_logging()
        LOG.info("Testing permissions")
    except Exception as error:
        sys.exit(
            "BigPanda Splunk: Invalid permissions detected: %s" % str(error))

    error = send_test_alert()
    if error:
        sys.exit(error)
    print 'BigPanda Splunk Integration Configured.\n\
Your should see a test alert at your BigPanda dashboard...'
