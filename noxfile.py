"""nox-poetry configuration file."""

import shlex

import nox
from loguru import logger
from nox_poetry import session
from nox_poetry.sessions import Session

from calcipy.doit_tasks.doit_globals import DIG


def configure_nox() -> None:
    """Toggle nox settings. Default is to set `error_on_missing_interpreters` to True."""
    nox.options.reuse_existing_virtualenvs = True
    nox.options.error_on_missing_interpreters = True


@session(python=[DIG.test.pythons], reuse_venv=True)
def tests(session: Session) -> None:
    """Run doit test task for specified python versions."""
    session.install('.[dev]', '.[test]')
    session.run(*shlex.split('poetry run doit run test'))


@session(python=[DIG.test.pythons[-1]], reuse_venv=False)
def build(session: Session) -> None:
    """Build the project files within a controlled environment for repeatability."""
    path_wheel = session.poetry.build_package()
    logger.info(path_wheel)
