"""Global variables for testing."""

from pathlib import Path

import snoop

TEST_DIR = Path(__file__).parent
"""Path to the `test` directory that contains this file and all other tests."""

TEST_DATA_DIR = TEST_DIR / 'data'
"""Path to subdirectory with test data within the Test Directory."""

TEST_SNOOPER = snoop.Config(out=TEST_DIR / 'test.log', overwrite=True)
"""Snoop configuration for logging to a test.log file in the test directory."""


# PLANNED: Output the test name and other information to the test.log file. Currently only used in `no_log_errors`
# PLANNED: move to dash_dev
def no_log_errors(dash_duo, suppressed_errors=None):
    """Return True if any unsuppressed errors found in console logs.

    Args:
        dash_duo: dash_duo instance
        suppressed_errors: list of suppressed error strings. Default is None to check for any log errors

    Returns:
        boolean: True if no unsuppressed errors found in dash logs

    """
    if suppressed_errors is None:
        suppressed_errors = []

    logs = TEST_SNOOPER.pp(dash_duo.get_logs())
    return not [log for log in logs if log['level'] not in suppressed_errors]
