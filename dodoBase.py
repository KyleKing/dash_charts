"""Base DoIt Tasks."""

import webbrowser
from pathlib import Path

import toml

# Configure Globals
TOML_PTH = Path.cwd() / 'pyproject.toml'
PKG_NAME = toml.load(TOML_PTH)['tool']['poetry']['name']

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


def task_updateCL():
    """Automate updating the Changelog file."""
    return debug_action(['gitchangelog > CHANGELOG-raw.md'])
