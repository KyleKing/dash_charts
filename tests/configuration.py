"""Global variables for testing."""

from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
"""Path to the `test` directory that contains this file and all other tests."""

TEST_DATA_DIR = TEST_DIR / 'data'
"""Path to subdirectory with test data within the Test Directory."""


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

    logs = dash_duo.get_logs()
    # logger.debug(logs)
    # HACK: get_logs always return None with webdrivers other than Chrome
    # FIXME: Handle path to the executable. Example with Firefox when the Gecko Drive is installed and on path
    # poetry run pytest tests -x -l --ff -vv --webdriver Firefox
    # Will one of these work?
    # - https://pypi.org/project/webdrivermanager/
    # - https://pypi.org/project/chromedriver-binary/
    # - https://pypi.org/project/undetected-chromedriver/
    # - https://pypi.org/project/webdriver-manager/
    #
    # Actually set DASH_TEST_CHROMEPATH? Maybe still use one of the above packages to get the path?
    # - https://github.com/plotly/dash/blob/5ef534943852f2d02a9da636cf18357c5df5b3e5/dash/testing/browser.py#L436
    return logs is None or not [log for log in logs if log['level'] not in suppressed_errors]
