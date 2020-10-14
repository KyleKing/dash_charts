"""DoIt Script. Run all tasks with `poetry run doit` or single task with `poetry run doit run update_cl`."""

from pathlib import Path

from dash_dev.doit_base import DIG, task_check_req, task_export_req  # noqa: F401
from dash_dev.doit_doc import (task_create_tag, task_document, task_open_docs, task_remove_tag,  # noqa: F401
                               task_update_cl)
from dash_dev.doit_lint import (task_auto_format, task_lint_pre_commit, task_lint_project,  # noqa: F401
                                task_radon_lint, task_set_lint_config)
from dash_dev.doit_test import (task_coverage, task_open_test_docs, task_ptw_current, task_ptw_ff,  # noqa: F401
                                task_ptw_marker, task_ptw_not_chrome, task_test, task_test_all, task_test_keyword,
                                task_test_marker)

# Configure Dash paths
DIG.set_paths(source_path=Path(__file__).parent.resolve())

# Create list of all tasks run with `poetry run doit`
DOIT_CONFIG = {
    'action_string_formatting': 'old',  # Required for keyword-based tasks
    'default_tasks': [
        'export_req', 'check_req', 'update_cl',  # Comment on/off as needed
        'set_lint_config',  # Comment on/off as needed
        'auto_format',  # Comment on/off as needed
        'lint_pre_commit',  # Comment on/off as needed
        'coverage',  # Comment on/off as needed
        # 'open_test_docs',  # Comment on/off as needed
        'document',  # Comment on/off as needed
        # 'open_docs',  # Comment on/off as needed
    ],
}
"""DoIt Configuration Settings. Run with `poetry run doit`."""
