"""DoIt Script. Run with `poetry run doit` or `poetry run doit run exportReq`."""

import shutil
from pathlib import Path

from dash_charts.base_dodo import PKG_NAME, debug_action, openInBrowser, task_exportReq, task_updateCL  # noqa: F401

# Create list of all tasks run with `poetry run doit`
DOIT_CONFIG = {'default_tasks': [
    'exportReq', 'updateCL', 'document', 'commitDocs',
]}

# Set documentation paths
DOC_DIR = Path.cwd() / 'docs'
STAGING_DIR = DOC_DIR / PKG_NAME
GH_PAGES_DIR = Path.cwd() / '../Dash_Charts_gh-pages'
assert GH_PAGES_DIR.is_dir(), 'Expected directory at: {}'.format(GH_PAGES_DIR)


def clearDocs():
    """Clear the documentation files from the directories."""
    for pth in list(STAGING_DIR.glob('*.html')) + list(GH_PAGES_DIR.glob('*.html')):
        pth.unlink()


def copyDocs():
    """Copy the documentation files from the staging to the output."""
    for pth in list(STAGING_DIR.glob('*.html')):
        shutil.copyfile(pth, GH_PAGES_DIR / pth.name)


def task_document():
    """Build the HTML documentation and push to gh-pages branch."""
    # Format the pdoc CLI args
    args = '{} --html --force --template-dir "{}" --output-dir "{}"'.format(PKG_NAME, DOC_DIR, DOC_DIR)
    return debug_action([
        (clearDocs, ()),
        'poetry run pdoc3 {}'.format(args),
        (copyDocs, ()),
    ])


def task_commitDocs():
    """Commit the documentation to gh-pages."""
    return debug_action([
        'cd {}; git add .; git commit -m "Chg: update pdoc files"; git push'.format(GH_PAGES_DIR),
    ])


def task_openDocs():
    """Open the documentation files in the default browser."""
    return debug_action([
        (openInBrowser, (STAGING_DIR / 'index.html',)),
    ])
