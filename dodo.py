"""DoIt Script. Run all tasks with `poetry run doit` or single task with `poetry run doit run update_cl`."""

import json
import re
import shutil
import tempfile
import webbrowser
from pathlib import Path

import toml
from icecream import ic
from transitions import Machine

TOML_PTH = Path(__file__).parent / 'pyproject.toml'
"""Path to `pyproject.toml` file."""

PKG_NAME = toml.load(TOML_PTH)['tool']['poetry']['name']
"""Name of the current package based on the poetry configuration file."""

# Create list of all tasks run with `poetry run doit`
DOIT_CONFIG = {
    'action_string_formatting': 'old',  # Required for keyword-based tasks
    'default_tasks': [
        'export_req', 'check_req', 'update_cl',  # Comment on/off as needed
        'lint',  # Comment on/off as needed
        'coverage',  # Comment on/off as needed
        'open_test_docs',  # Comment on/off as needed
        'document',  # Comment on/off as needed
        'open_docs',  # Comment on/off as needed
        'commit_docs',  # Comment on/off as needed
    ],
}
"""DoIt Configuration Settings. Run with `poetry run doit`."""

# Set global paths
CWD = Path(__file__).parent
FLAKE8_PATH = CWD / '.flake8'
DOC_DIR = CWD / 'docs'
STAGING_DIR = DOC_DIR / PKG_NAME
SRC_EXAMPLES_DIR = CWD / 'tests/examples'
TMP_EXAMPLES_DIR = CWD / f'{PKG_NAME}/0EX'

GH_PAGES_DIR = Path(__file__).parents[1] / 'Dash_Charts_gh-pages'
if not GH_PAGES_DIR.is_dir():
    raise RuntimeError(f'Expected directory at: {GH_PAGES_DIR}')

# ----------------------------------------------------------------------------------------------------------------------
# General DoIt Utilities


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


def if_found_unlink(file_path):
    """Remove file if it exists. Function is intended to a DoIt action.

    Args:
        file_path: Path to file to remove

    """
    if file_path.is_file():
        file_path.unlink()

# ----------------------------------------------------------------------------------------------------------------------
# Manage Requirements


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

# ----------------------------------------------------------------------------------------------------------------------
# Linting


def check_linting_errors(flake8_log_path):
    """Check for errors reported in flake8 log file. Removes log file if no errors detected.

    Args:
        flake8_log_path: path to flake8 log file created with flag: `--output-file=flake8_log_path`

    Raises:
        RuntimeError: if flake8 log file contains any text results

    """
    if len(flake8_log_path.read_text().strip()) > 0:
        raise RuntimeError(f'Found Linting Errors. Review: {flake8_log_path}')
    if_found_unlink(flake8_log_path)


def lint(path_list, flake8_path=FLAKE8_PATH):
    """Lint specified files creating summary log file of errors.

    Args:
        path_list: list of file paths to lint
        flake8_path: path to flake8 configuration file. Default is `FLAKE8_PATH`

    Returns:
        dict: DoIt task

    """
    flake8_log_path = CWD / 'flake8.log'
    flags = f'--config={flake8_path}  --output-file={flake8_log_path} --exit-zero'
    return debug_action([
        (if_found_unlink, (flake8_log_path, )),
        *[f'poetry run flake8 "{fn}" {flags}' for fn in path_list],
        (check_linting_errors, (flake8_log_path, )),
    ])


def task_lint():
    """Configure linting as a task.

    Returns:
        dict: DoIt task

    """
    path_list = [*CWD.glob('*.py')]
    for base_path in [CWD / PKG_NAME, CWD / 'tests']:
        path_list.extend([*base_path.glob('**/*.py')])
    ic(path_list)
    return lint(path_list)

# ----------------------------------------------------------------------------------------------------------------------
# Manage Changelog


def task_update_cl():
    """Update a Changelog file with the raw Git history.

    Returns:
        dict: DoIt task

    """
    return debug_action(['gitchangelog > CHANGELOG-raw.md'])


def task_create_tag():
    """Create a git tag based on the version in pyproject.toml.

    Returns:
        dict: DoIt task

    """
    version = toml.load(TOML_PTH)['tool']['poetry']['version']
    message = 'New Revision from PyProject.toml'
    return debug_action([
        f'git tag -a {version} -m "{message}"',
        'git tag -n10 --list',
        'git push origin --tags',
    ])


def task_remove_tag():
    """Delete tag for current version in pyproject.toml.

    Returns:
        dict: DoIt task

    """
    version = toml.load(TOML_PTH)['tool']['poetry']['version']
    return debug_action([
        f'git tag -d "{version}"',
        'git tag -n10 --list',
        f'git push origin :refs/tags/{version}',
    ])


# ----------------------------------------------------------------------------------------------------------------------
# Manage Documentation


def clear_docs():
    """Clear the documentation directory before running pdoc."""
    if STAGING_DIR.is_dir():
        shutil.rmtree(STAGING_DIR)


def stage_documentation():
    """Copy the documentation files from the staging to the output."""
    tmp_dir = Path(tempfile.mkdtemp())
    (GH_PAGES_DIR / '.git').rename(tmp_dir / '.git')
    try:
        shutil.rmtree(GH_PAGES_DIR)
        shutil.copytree(STAGING_DIR, GH_PAGES_DIR)
        (GH_PAGES_DIR / 'README.md').write_text(f"""# {PKG_NAME.upper()} Documentation Site
See `master` branch for latest code. This branch is auto-generated by pdoc""")
    finally:
        (tmp_dir / '.git').rename(GH_PAGES_DIR / '.git')
        shutil.rmtree(tmp_dir)


def stage_examples():
    """Format the code examples as docstrings to be loaded into the documentation."""
    TMP_EXAMPLES_DIR.mkdir(exist_ok=False)
    (TMP_EXAMPLES_DIR / '__init__.py').write_text('"""Code Examples (documentation-only, not in package)."""')
    for file_path in SRC_EXAMPLES_DIR.glob('*.py'):
        content = file_path.read_text().replace('"', r'\"')  # read and escape quotes
        dest_fn = TMP_EXAMPLES_DIR / file_path.name
        docstring = f'From file: `{file_path.relative_to(CWD.parent)}`'
        dest_fn.write_text(f'"""{docstring}\n```\n{content}\n```\n"""')


def clear_examples():
    """Clear the examples from within the package directory."""
    shutil.rmtree(TMP_EXAMPLES_DIR)


class ReadMeMachine:
    """State machine to replace commented sections of readme with new text."""

    states = ['readme', 'new']

    transitions = [
        {'trigger': 'start_new', 'source': 'readme', 'dest': 'new'},
        {'trigger': 'end', 'source': 'new', 'dest': 'readme'},
    ]

    readme_lines: list = None

    def __init__(self):
        """Initialize state machine."""
        self.machine = Machine(model=self, states=ReadMeMachine.states, initial='readme',
                               transitions=ReadMeMachine.transitions)

    def parse(self, lines, comment_pattern, new_text):
        """Parse lines and insert new_text.

        Args:
            lines: list of text files
            comment_pattern: comment pattern to match (ex: ``)
            new_text: dictionary with comment string as key

        Returns:
            list: list of strings for README

        """
        self.readme_lines = []
        for line in lines:
            if comment_pattern.match(line):
                self.readme_lines.append(line)
                if line.strip().startswith('<!-- /'):
                    self.end()
                else:
                    key = comment_pattern.match(line).group(1)
                    self.readme_lines.extend(['', *new_text[key], ''])
                    self.start_new()
            elif self.state == 'readme':
                self.readme_lines.append(line)

        return self.readme_lines


def write_to_readme(comment_pattern, new_text):
    """Wrapper method for ReadMeMachine. Handles reading then writing changes to the README.

    Args:
        comment_pattern: comment pattern to match (ex: ``)
        new_text: dictionary with comment string as key

    """
    readme_path = CWD / 'README.md'
    lines = readme_path.read_text().split('\n')
    readme_lines = ReadMeMachine().parse(lines, comment_pattern, new_text)
    readme_path.write_text('\n'.join(readme_lines))


def write_code_to_readme():
    """Replace commented sections in README with linked file contents."""
    comment_pattern = re.compile(r'\s*<!-- /?(CODE:.*) -->')
    fn = 'tests/examples/readme.py'
    source_code = ['```py', *(CWD / fn).read_text().split('\n'), '```']
    new_text = {f'CODE:{fn}': [f'    {line}'.rstrip() for line in source_code]}
    write_to_readme(comment_pattern, new_text)


def write_coverage_to_readme():
    """Read the coverage.json file and write a Markdown table to the README file."""
    # Read coverage information from json file
    coverage = json.loads((CWD / 'coverage.json').read_text())
    # Collect raw data
    legend = ['File', 'Statements', 'Missing', 'Excluded', 'Coverage']
    int_keys = ['num_statements', 'missing_lines', 'excluded_lines']
    rows = [legend, ['--:'] * len(legend)]
    for file_path, file_obj in coverage['files'].items():
        rows.append([file_path.replace('dash_charts/', '')]
                    + [file_obj['summary'][key] for key in int_keys]
                    + [round(file_obj['summary']['percent_covered'], 1)])
    # Format table for Github Markdown
    table_lines = [f"| {' | '.join([str(value) for value in row])} |" for row in rows]
    table_lines.extend(['', f"Generated on: {coverage['meta']['timestamp']}"])
    # Replace coverage section in README
    comment_pattern = re.compile(r'<!-- /?(COVERAGE) -->')
    write_to_readme(comment_pattern, {'COVERAGE': table_lines})


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
        (write_code_to_readme, ()),
        'coverage json',  # creates 'coverage.json' file
        (write_coverage_to_readme, ()),
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


# ----------------------------------------------------------------------------------------------------------------------
# Manage Testing


def task_test():
    """Run tests with Pytest.

    Returns:
        dict: DoIt task

    """
    return debug_action([
        f'poetry run pytest "{CWD}" -x -l --ff -v',
    ], verbosity=2)


def task_coverage():
    """Run pytest and create coverage and test reports.

    Returns:
        dict: DoIt task

    """
    coverage_dir = DOC_DIR / 'coverage_html'
    test_report_path = DOC_DIR / 'test_report.html'
    return debug_action([
        (f'poetry run pytest "{CWD}" -x -l --ff -v --cov-report=html:"{coverage_dir}" --cov={PKG_NAME}'
         f' --html="{test_report_path}" --self-contained-html'),
    ], verbosity=2)


def task_open_test_docs():
    """Open the test and coverage files in default browser.

    Returns:
        dict: DoIt task

    """
    return debug_action([
        (open_in_browser, (DOC_DIR / 'coverage_html/index.html',)),
        (open_in_browser, (DOC_DIR / 'test_report.html',)),
    ])


def task_test_marker():
    r"""Specify a marker to run a subset of tests.

    Example: `doit run test_marker -m \"not MARKER\"` or `doit run test_marker -m \"MARKER\"`

    Returns:
        dict: DoIt task

    """
    return {
        'actions': [f'poetry run pytest "{CWD}" -x -l --ff -v -m "%(marker)s"'],
        'params': [{
            'name': 'marker', 'short': 'm', 'long': 'marker', 'default': '',
            'help': ('Runs test with specified marker logic\nSee: '
                     'https://docs.pytest.org/en/latest/example/markers.html?highlight=-m'),
        }],
        'verbosity': 2,
    }


def task_test_keyword():
    r"""Specify a keyword to run a subset of tests.

    Example: `doit run test_keyword -k \"KEYWORD\"`

    Returns:
        dict: DoIt task

    """
    return {
        'actions': [f'poetry run pytest "{CWD}" -x -l --ff -v -k "%(keyword)s"'],
        'params': [{
            'name': 'keyword', 'short': 'k', 'long': 'keyword', 'default': '',
            'help': ('Runs only tests that match the string pattern\nSee: '
                     'https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests'),
        }],
        'verbosity': 2,
    }
