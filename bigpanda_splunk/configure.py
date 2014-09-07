from bigpanda_splunk import \
        SPLUNK_HOME, \
        SCRIPT_NAME, \
        LOG, write_config, setup_logging, get_path
from bigpanda_splunk.runner import send_test_alert

import glob
import grp
import os
import pwd
import sys

SPLUNK_USER_NAME = "splunk"

GID, UID = None, None

try:
    GID = grp.getgrnam(SPLUNK_USER_NAME).gr_gid
    UID = pwd.getpwnam(SPLUNK_USER_NAME).pw_uid
except:
    pass

def configure(runner_path, params):
    """
    Configure BigPanda Splunk Provider
    """
    if not params or len(params) < 3:
        return sys.exit("BigPanda Splunk\nUsage: %s TOKEN APP_KEY" % os.path.basename(runner_path))
    token, app_key = params[1], params[2]
    if not os.path.exists(SPLUNK_HOME):
        return sys.exit("BigPanda Splunk: Splunk installation not found!")

    runner_dir = os.path.dirname(runner_path)

    try:
        bp_shell_path = get_path(SCRIPT_NAME)
        if os.path.exists(bp_shell_path):
            os.unlink(bp_shell_path)
        bp_shell_content = """#!/bin/bash
PYTHONPATH= LD_LIBRARY_PATH= %s %s $@[]
""" % (sys.executable, os.path.join(runner_dir, SCRIPT_NAME))
        with open(bp_shell_path, "w") as shell_file:
            shell_file.write(bp_shell_content)
        write_config(token, app_key)
        setup_logging()
        LOG.info("Testing permissions")
        if GID and UID:
            for bp_file in glob.glob(get_path('') + "/bigpanda*"):
                os.chown(bp_file, UID, GID)
    except Exception as error:
        return sys.exit(
            "BigPanda Splunk: Invalid permissions detected: %s" % str(error))

    error = send_test_alert()
    if error:
        return sys.exit(error)
    print 'BigPanda Splunk Integration Configured.\n\
Your should see a test alert at your BigPanda dashboard...'
