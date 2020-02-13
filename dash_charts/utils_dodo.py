"""DoIt Utilities and Tasks."""

import webbrowser
from pathlib import Path

import toml
from icecream import ic

# TODO: Add function to set git tags for version control

TOML_PTH = Path(__file__).parents[1] / 'pyproject.toml'
"""Path to `pyproject.toml` file."""

PKG_NAME = toml.load(TOML_PTH)['tool']['poetry']['name']
"""Name of the current package based on the poetry configuration file."""


def show_cmd(task):
    """For debugging, log the full command to the console.

    Args:
        task: task dictionary passed by DoIt

    Returns:
        str: describing the sequence of actions

    """
    actions = ''.join([f'\n\t{act}' for act in task.actions])
    return f'{task.name} > [{actions}\n]\n'


def debug_action(actions, verbosity=2):
    """Enable verbose logging for the specified actions.

    Args:
        actions: list of DoIt actions
        verbosity: 2 is maximum, while 0 is disabled

    Returns:
        dict: keys `actions`, `title`, and `verbosity` for dict: DoIt task

    """
    return {
        'actions': actions,
        'title': show_cmd,
        'verbosity': verbosity,
    }


def open_in_browser(file_path):
    """Open the path in the default web browser.

    Args:
        file_path: Path to file

    """
    webbrowser.open(Path(file_path).as_uri())


def task_export_req():
    """Create a `requirements.txt` file for non-Poetry users and for Github security tools.

    Returns:
        dict: DoIt task

    """
    req_path = TOML_PTH.parent / 'requirements.txt'
    return debug_action([f'poetry export -f {req_path.name} -o "{req_path}" --without-hashes --dev'])


def dump_pur_results(pur_path):
    """Write the contents of the `pur` output file to STDOUT with icecream.

    Args:
        pur_path: Path to the pur output text file

    """
    ic(pur_path.read_text())


def task_check_req():
    """Use pur to check for the latest versions of available packages.

    Returns:
        dict: DoIt task

    """
    req_path = TOML_PTH.parent / 'requirements.txt'
    pur_path = TOML_PTH.parent / 'tmp.txt'
    return debug_action([
        f'poetry run pur -r "{req_path}" > "{pur_path}"',
        (dump_pur_results, (pur_path, )),
        (Path(pur_path).unlink, ),
    ])


def task_update_cl():
    """Update a Changelog file with the raw Git history.

    Returns:
        dict: DoIt task

    """
    return debug_action(['gitchangelog > CHANGELOG-raw.md'])


def task_create_tag():
    """Create a git tag based on the version in pyproject.toml."""
    version = toml.load(TOML_PTH)['tool']['poetry']['version']
    message = "New Revision from PyProject.toml"
    return debug_action([
        f'git tag -a {version} -m "{message}"',
        'git tag -n10 --list',
        'git push origin --tags',
    ])


def task_remove_tag():
    """Delete tag for current version in pyproject.toml."""
    version = toml.load(TOML_PTH)['tool']['poetry']['version']
    return debug_action([
        f'git tag -d "{version}"',
        'git tag -n10 --list',
        f'git push origin :refs/tags/{version}',
    ])
