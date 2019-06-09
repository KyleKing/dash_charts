"""DoIt Script. Run with `poetry run doit` or `poetry run doit run exportReq`."""

DOIT_CONFIG = {'default_tasks': [
    'exportReq',
]}


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


def task_exportReq():
    """Export a requirements.txt file for Github security checking."""
    return debug_action(['poetry export -f requirements.txt --without-hashes --dev'])
