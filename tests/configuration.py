"""Global variables for testing."""

from pathlib import Path

from calcipy import __pkg_name__
from calcipy.log_helpers import build_logger_config
from loguru import logger

TEST_DIR: Path = Path(__file__).resolve().parent
"""Path to the `test` directory that contains this file and all other tests."""

TEST_DATA_DIR: Path = TEST_DIR / 'data'
"""Path to subdirectory with test data within the Test Directory."""

# PLANNED: Move all of this into a function! (and/or task?) {Duplicate of dodo.py}

logger.enable(__pkg_name__)  # This will enable output from calcipy, which is off by default
# See an example of toggling loguru at: https://github.com/KyleKing/calcipy/tree/examples/loguru-toggle

path_project = Path(__file__).resolve().parent
log_config = build_logger_config(path_project, production=False)
logger.configure(**log_config)
logger.info(
    'Started logging to {path_project}/.logs with {log_config}', path_project=path_project,
    log_config=log_config,
)


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
