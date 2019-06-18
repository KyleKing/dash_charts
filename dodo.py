"""DoIt Script. Run with `poetry run doit` or `poetry run doit run exportReq`."""

from pathlib import Path

import toml

# Configure Globals
TOML_PTH = Path.cwd() / 'pyproject.toml'
PKG_NAME = toml.load(TOML_PTH)['tool']['poetry']['name']
# Create list of all tasks run with `poetry run doit`
DOIT_CONFIG = {'default_tasks': [
    'exportReq',
]}

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


# ------------------
# Tasks


def task_exportReq():
    """Export a requirements.txt file for Github security checking."""
    return debug_action(['poetry export -f requirements.txt --without-hashes --dev'])


def task_document():
    """Build the HTML documentation."""
    docDir = Path.cwd() / 'docs'
    args = '{} --html --force'.format(PKG_NAME)
    tempDir = '--template-dir "{}"'.format(docDir)
    outDir = '--output-dir "{}"'.format(docDir)
    return debug_action([
        'poetry run pdoc3 {} {} {}'.format(args, tempDir, outDir),
    ])
    # TODO: Copy the output HTML files from docs/dash_charts/*.html to
    #   the separate gh-pages repo and push

    # Create a clean gh-pages branch
    # git checkout --orphan gh-pages
    # git rm -rf --dry-run .
    # git rm -rf .
