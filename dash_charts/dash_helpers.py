"""Helpers for building Dash applications."""

import argparse
import csv
import json
import sqlite3
import time
from contextlib import ContextDecorator
from datetime import datetime
from pathlib import Path

import dataset
from cerberus import Validator


def validate(document, schema, **validator_kwargs):
    """Validate a data structure. Return errors if any found.

    Cerberus Documentation: https://docs.python-cerberus.org/en/stable/validation-rules.html

    Args:
        document: data structure to validate
        schema: expected structure
        validator_kwargs: additional keyword arguments for Validator class

    Returns:
        list: validation errors

    """
    validator = Validator(schema, **validator_kwargs)
    validator.validate(document)
    return validator.errors


def parse_dash_cli_args():  # pragma: no cover
    """Configure the CLI options for Dash applications.

    Returns:
        dict: keyword arguments for Dash

    """
    parser = argparse.ArgumentParser(description='Process Dash Parameters.')
    parser.add_argument('--port', type=int, default=8050,
                        help='Pass port number to Dash server. Default is 8050')
    parser.add_argument('--nodebug', action='store_true', default=False,
                        help='If set, will disable debug mode. Default is to set `debug=True`')
    args = parser.parse_args()
    return {'port': args.port, 'debug': not args.nodebug}


def json_dumps_compact(data):
    """Format provided dictionary into compact JSON. Lists will be in one line rather than split on new lines.

    Args:
        data: JSON-serializable dictionary

    Returns:
        str: JSON-formatted string with lists compacted into a single line

    """
    clean_data = {}
    # Check each key/value pair to determine if any intermediary strings are needed for later formatting
    for key, raw in data.items():
        if isinstance(raw, list):
            values = [f'``{value}``' if isinstance(value, str) else value for value in raw]
            clean_data[key] = '[' + ','.join(map(str, values)) + ']'
        else:
            clean_data[key] = raw
    # Format the dictionary into JSON and replace the special characters used as intermediaries
    raw_json = json.dumps(clean_data, indent=4, separators=(',', ': '), sort_keys=True)
    return (raw_json
            .replace(': "[', ': [')
            .replace(']"', ']')
            .replace('``', '"')
            .replace("'", '"'))


def write_pretty_json(filename, obj):
    """Write indented JSON file.

    Args:
        filename: Path or plain string filename to write (should end with `.json`)
        obj: JSON object to write

    """
    Path(filename).write_text(json.dumps(obj, indent=4, separators=(',', ': ')))


class SQLConnection(ContextDecorator):
    """Ensure the SQLite connection is properly opened and closed."""

    def __init__(self, db_file):
        """Initialize context wrapper.

        Args:
            db_file: Path to SQLite file

        """
        self.conn = None
        self.db_file = db_file

    def __enter__(self):
        """Connect to the database and return connection reference.

        Returns:
            dict: connection to sqlite database

        """
        self.conn = sqlite3.connect(self.db_file)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection."""  # noqa: DAR101
        self.conn.close()


class DBConnect:
    """Manage database connection since closing connection isn't possible."""

    database_path = None
    """Path to the local storage SQLite database file. Initialize in `__init__()`."""

    _db = None

    @property
    def db(self):
        """Return connection to database. Will create new connection if one does not exist already.

        Returns:
            dict: `dataset` database instance

        """
        if self._db is None:
            self._db = dataset.connect(f'sqlite:///{self.database_path}')
        return self._db

    def __init__(self, database_path):
        """Store the database path and ensure the parent directory exists.

        Args:
            database_path: path to the SQLite file

        """
        self.database_path = database_path.resolve()
        self.database_path.parent.mkdir(exist_ok=True)


def rm_brs(line):
    """Replace all whitespace (line breaks, etc) with spaces."""  # noqa: DAR101,DAR201
    return ' '.join(line.split())


def uniq_table_id():
    """Return a unique table ID based on the current time in ms.

    Returns:
        str: in format `U<timestamp_ns>`

    """
    return f'U{time.time_ns()}'


def export_table_as_csv(csv_filename, table):
    """Create a CSV file summarizing a table of a dataset database.

    Args:
        csv_filename: Path to csv file
        table: table from dataset database

    """
    with open(csv_filename, 'w', newline='\n', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(table.columns)
        for row in table:
            writer.writerow([*row.values()])


def graph_return(resp, keys):
    """Based on concepts of GraphQL, return specified subset of response.

    Args:
        resp: dictionary with values from function
        keys: list of keynames from the resp dictionary

    Returns:
        the `resp` dictionary with only the keys specified in the `keys` list

    Raises:
        RuntimeError: if `keys` is not a list or tuple

    """
    if not (len(keys) and isinstance(keys, (list, tuple))):
        raise RuntimeError(f'Expected list of keys for: `{resp.items()}`, but received `{keys}`')
    ordered_responses = [resp.get(key, None) for key in keys]
    return ordered_responses if len(ordered_responses) > 1 else ordered_responses[0]


def get_unix(str_ts, date_format):
    """Get unix timestamp from a string timestamp in date_format.

    Args:
        str_ts: string timestamp in `date_format`
        date_format: datetime time stamp format

    Returns:
        int: unix timestamp

    """
    return datetime.strptime(str_ts, date_format).timestamp()


def format_unix(unix_ts, date_format):
    """Format unix timestamp as a string timestamp in date_format.

    Args:
        unix_ts: unix timestamp
        date_format: datetime time stamp format

    Returns:
        string: formatted timestamp in `date_format`

    """
    return datetime.fromtimestamp(unix_ts).strftime(date_format)
