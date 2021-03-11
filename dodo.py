"""doit Script.

```sh
# Ensure that packages are installed
poetry install
# List Tasks
poetry run doit list
# (Or use a poetry shell)
# > poetry shell
# > doit list

# Run tasks individually (examples below)
poetry doit run coverage open_test_docs
poetry doit run set_lint_config create_tag_file document
# Or all of the tasks in DOIT_CONFIG
poetry run doit
```

"""

from pathlib import Path

from calcipy import __pkg_name__
from calcipy.doit_tasks import *  # noqa: F401,F403,H303 (Run 'doit list' to see tasks). skipcq: PYL-W0614
from calcipy.doit_tasks import DOIT_CONFIG_RECOMMENDED
from calcipy.doit_tasks.base import debug_task
from calcipy.doit_tasks.doit_globals import DIG
from calcipy.log_helpers import build_logger_config
from loguru import logger

# PLANNED: Move all of this into a function! (and/or task?)

logger.enable(__pkg_name__)  # This will enable output from calcipy, which is off by default
# See an example of toggling loguru at: https://github.com/KyleKing/calcipy/tree/examples/loguru-toggle

path_project = Path(__file__).resolve().parent
log_config = build_logger_config(path_project, production=False)
logger.configure(**log_config)
logger.info(
    'Started logging to {path_project}/.logs with {log_config}', path_project=path_project,
    log_config=log_config,
)

# Create list of all tasks run with `poetry run doit`
DOIT_CONFIG = DOIT_CONFIG_RECOMMENDED


def task_write_puml():
    """Write updated PlantUML file(s) with `py2puml`."""
    pkg = DIG.meta.pkg_name
    diagram_dir = DIG.meta.path_project / '.diagrams'

    # TODO: pypi package wasn't working. Used local version
    run_py2puml = f'poetry run ../py-puml-tools/py2puml/py2puml.py --config {diagram_dir}/py2puml.ini'

    # # PLANNED: needs to be a bit more efficient...
    # > files = []
    # > for file_path in (DIG.source_path / pkg).glob('*.py'):
    # >     if any(line.startswith('class ') for line in file_path.read_text().split('\n')):
    # >         files.append(file_path.name)
    files = [
        'utils_app.py',
        'utils_app_modules.py',
        'utils_app_with_navigation.py',
        'utils_fig.py',
    ]
    return debug_task([
        f'{run_py2puml} -o {diagram_dir}/{pkg}.puml' + ''.join([f' {pkg}/{fn}' for fn in files]),
        f'plantuml {diagram_dir}/{pkg}.puml -tpng',
        # f'plantuml {diagram_dir}/{pkg}.puml -tsvg',

        # > f'{run_py2puml} -o {diagram_dir}/{pkg}-examples.puml ./tests/examples/*.py --root ./tests',
        # > f'plantuml {diagram_dir}/{pkg}-examples.puml -tsvg',
    ])
