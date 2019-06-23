"""DoIt Script. Run with `poetry run doit` or `poetry run doit run exportReq`."""

import shutil
import webbrowser
from pathlib import Path

import toml

# Create list of all tasks run with `poetry run doit`
DOIT_CONFIG = {'default_tasks': [
    'exportReq', 'updateCL', 'document', 'commitDocs',
]}

# Configure Globals
TOML_PTH = Path.cwd() / 'pyproject.toml'
PKG_NAME = toml.load(TOML_PTH)['tool']['poetry']['name']

# Determine documentation paths
DOC_DIR = Path.cwd() / 'docs'
STAGING_DIR = DOC_DIR / PKG_NAME
GH_PAGES_DIR = Path.cwd() / '../Dash_Charts_gh-pages'
assert GH_PAGES_DIR.is_dir(), 'Expected directory at: {}'.format(GH_PAGES_DIR)


# ------------------
# DoIt Utilities

def show_cmd(task):
    """For debugging, log the full command to the console.

    task -- task dictionary passed by DoIt

    """
    return '{} > [{}\n]\n'.format(task.name, ''.join(['\n\t{}'.format(act) for act in task.actions]))


def debug_action(actions, verb=2):
    """Enable verbose logging for the specified actions.

    actions -- list of DoIt actions
    verbosity -- 2 is maximum, while 0 is disabled

    """
    return {
        'actions': actions,
        'title': show_cmd,
        'verbosity': verb,
    }


def openInBrowser(pth):
    """Open the path in the default web browser)."""
    webbrowser.open('file:///{}'.format(pth))


# ------------------
# Tasks


def task_exportReq():
    """Export a requirements.txt file for Github security checking."""
    return debug_action(['poetry export -f requirements.txt --without-hashes --dev'])


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
        'cd {}; git add .; git commit -m "Add: pdoc files"; git push'.format(GH_PAGES_DIR),
    ])


def task_openDocs():
    """Open the documentation files in the default browser."""
    return debug_action([
        (openInBrowser, (STAGING_DIR / 'index.html',)),
    ])


def task_updateCL():
    """Automate updating the Changelog file."""
    return debug_action(['gitchangelog > CHANGELOG.md'])
