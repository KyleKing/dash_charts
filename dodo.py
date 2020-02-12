"""DoIt Script. Run with `poetry run doit` or `poetry run doit run exportReq`."""

import shutil
from pathlib import Path

from dash_charts.utils_dodo import (PKG_NAME, debug_action, open_in_browser, task_check_req,  # noqa: F401
                                    task_export_req, task_update_cl)

# Create list of all tasks run with `poetry run doit`
DOIT_CONFIG = {'default_tasks': [
    'export_req', 'check_req', 'update_cl', 'document',
    # 'commit_docs',  # Optionally comment to remove from task list
]}

# Set documentation paths
DOC_DIR = Path(__file__).parent / 'docs'
STAGING_DIR = DOC_DIR / PKG_NAME

GH_PAGES_DIR = Path(__file__).parents[1] / 'Dash_Charts_gh-pages'
if not GH_PAGES_DIR.is_dir():
    raise RuntimeError(f'Expected directory at: {GH_PAGES_DIR}')


def clear_docs():
    """Clear the documentation files from the directories."""
    for dir_path in [STAGING_DIR, GH_PAGES_DIR]:
        for file_path in dir_path.glob('*.html'):
            file_path.unlink()


def copy_docs():
    """Copy the documentation files from the staging to the output."""
    for file_path in list(STAGING_DIR.glob('*.html')):
        shutil.copyfile(file_path, GH_PAGES_DIR / file_path.name)


def task_document():
    """Build the HTML documentation and push to gh-pages branch.

    Returns:
        DoIt task

    """
    # Format the pdoc CLI args
    args = f'{PKG_NAME} --html --force --template-dir "{DOC_DIR}" --output-dir "{DOC_DIR}"'
    return debug_action([
        (clear_docs, ()),
        f'poetry run pdoc3 {args}',
        (copy_docs, ()),
    ])


def task_commit_docs():
    """Commit the documentation to gh-pages.

    Returns:
        DoIt task

    """
    return debug_action([
        f'cd {GH_PAGES_DIR}; git add .; git commit -m "Chg: update pdoc files"; git push',
    ])


def task_open_docs():
    """Open the documentation files in the default browser.

    Returns:
        DoIt task

    """
    return debug_action([
        (open_in_browser, (STAGING_DIR / 'index.html',)),
    ])
