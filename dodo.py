"""DoIt Script. Run all tasks with `poetry run doit` or single task with `poetry run doit run update_cl`."""

from pathlib import Path

# Third party
from dash_dev import doit_lint
from dash_dev.doit_base import DIG, task_check_req, task_export_req  # noqa: F401
from dash_dev.doit_doc import (task_create_tag, task_document, task_open_docs, task_remove_tag,  # noqa: F401
                               task_update_cl)
from dash_dev.doit_lint import task_auto_format, task_lint, task_radon_lint  # noqa: F401
from dash_dev.doit_test import (task_coverage, task_open_test_docs, task_ptw_current, task_ptw_ff,  # noqa: F401
                                task_ptw_not_chrome, task_test, task_test_keyword, task_test_marker)

# Configure Dash paths
DIG.set_paths(Path(__file__).parent)

# Create list of all tasks run with `poetry run doit`
DOIT_CONFIG = {
    'action_string_formatting': 'old',  # Required for keyword-based tasks
    'default_tasks': [
        'export_req', 'check_req', 'update_cl',  # Comment on/off as needed
        'auto_format',  # Comment on/off as needed
        'lint_pre_commit',  # Comment on/off as needed
        'coverage',  # Comment on/off as needed
        'open_test_docs',  # Comment on/off as needed
        'document',  # Comment on/off as needed
        'open_docs',  # Comment on/off as needed
    ],
}
"""DoIt Configuration Settings. Run with `poetry run doit`."""


def task_lint_pre_commit():
    """Create linting task that is more relaxed and just catches linting errors that I do not want on Github.

    Returns:
        dict: DoIt task

    """
    path_list = doit_lint.glob_path_list(dir_names=['examples', 'scripts'])
    return doit_lint.lint(path_list, ignore_errors=['E800', 'T100'])
