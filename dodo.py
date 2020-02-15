"""DoIt Script. Run all tasks with `poetry run doit` or single task with `poetry run doit run update_cl`."""

import shutil
from pathlib import Path

from dash_charts.utils_dodo import (PKG_NAME, debug_action, open_in_browser, task_check_req,  # noqa: F401
                                    task_create_tag, task_export_req, task_remove_tag, task_update_cl)

# PLANNED: use this regex to check for return formatting issues `Returns:\n\s+\S+[^:]\s`

# Create list of all tasks run with `poetry run doit`
DOIT_CONFIG = {
    'action_string_formatting': 'old',  # Required for keyword-based tasks
    'default_tasks': [
        'export_req', 'check_req', 'update_cl', 'document',  # Comment on/off as needed
        'open_docs',  # Comment on/off as needed
        'commit_docs',  # Comment on/off as needed
    ],
}

# Set documentation paths
GIT_DIR = Path(__file__).parent
DOC_DIR = GIT_DIR / 'docs'
STAGING_DIR = DOC_DIR / PKG_NAME
TMP_EXAMPLES_DIR = GIT_DIR / 'dash_charts/0EX'

GH_PAGES_DIR = Path(__file__).parents[1] / 'Dash_Charts_gh-pages'
if not GH_PAGES_DIR.is_dir():
    raise RuntimeError(f'Expected directory at: {GH_PAGES_DIR}')


def clear_docs():
    """Clear the documentation files from the directories."""
    for dir_path in [STAGING_DIR, GH_PAGES_DIR]:
        for file_path in dir_path.glob('*.html'):
            file_path.unlink()


def stage_documentation():
    """Copy the documentation files from the staging to the output."""
    for file_path in list(STAGING_DIR.glob('*.html')):
        shutil.copyfile(file_path, GH_PAGES_DIR / file_path.name)


def stage_examples():
    """Format the code examples as docstrings to be loaded into the documentation."""
    TMP_EXAMPLES_DIR.mkdir(exist_ok=False)
    (TMP_EXAMPLES_DIR / '__init__.py').write_text('"""Code Examples (documentation-only, not in `dash_charts`)."""')
    for file_path in (GIT_DIR / 'examples').glob('*.py'):
        content = file_path.read_text().replace('"', r'\"')  # read and escape quotes
        dest_fn = TMP_EXAMPLES_DIR / file_path.name
        docstring = f'From file: `{file_path.relative_to(GIT_DIR.parent)}`'
        dest_fn.write_text(f'"""{docstring}\n```\n{content}\n```\n"""')


def clear_examples():
    """Clear the examples from within the dash_charts package."""
    shutil.rmtree(TMP_EXAMPLES_DIR)


def task_document():
    """Build the HTML documentation and push to gh-pages branch.

    Returns:
        dict: DoIt task

    """
    # Format the pdoc CLI args
    args = f'{PKG_NAME} --html --force --template-dir "{DOC_DIR}" --output-dir "{DOC_DIR}"'
    return debug_action([
        (clear_docs, ()),
        (stage_examples, ()),
        f'poetry run pdoc3 {args}',
        (clear_examples, ()),
        (stage_documentation, ()),
    ])


def task_commit_docs():
    """Commit the documentation to gh-pages.

    Returns:
        dict: DoIt task

    """
    return debug_action([
        f'cd {GH_PAGES_DIR}; git add .; git commit -m "Chg: update pdoc files"; git push',
    ])


def task_open_docs():
    """Open the documentation files in the default browser.

    Returns:
        dict: DoIt task

    """
    return debug_action([
        (open_in_browser, (STAGING_DIR / 'index.html',)),
    ])
