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
import pandas as pd
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


# ----------------------------------------------------------------------------------------------------------------------
# sqlite3


class SQLConnection(ContextDecorator):
    """Ensure the SQLite connection is properly opened and closed."""

    def __init__(self, db_file):
        """Initialize context wrapper.

        Args:
            db_file: Path to a SQLite file

        """
        self.conn = None
        self.database_path = db_file

    def __enter__(self):
        """Connect to the database and return connection reference.

        Returns:
            dict: connection to sqlite database

        """
        self.conn = sqlite3.connect(self.database_path)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection."""  # noqa: DAR101
        self.conn.close()


def list_sql_tables(db_file):
    """Return all table names from the SQL database.

    Args:
        db_file: path to SQLite database file

    Returns:
        list: of unique table names in the SQL database

    """
    with SQLConnection(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE TYPE = "table"')
        return [names[0] for names in cursor.fetchall()]


# ----------------------------------------------------------------------------------------------------------------------
# dataset

META_TABLE_NAME = 'meta'
"""Name of the Meta-Data table in a typical SQLite database."""


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
            database_path: Path to the SQLite file

        """
        self.database_path = database_path.resolve()
        self.database_path.parent.mkdir(exist_ok=True)

    def new_table(self, table_name):
        """Create a table. Drop a table if one existed before.

        Args:
            table_name: string table name to create

        Returns:
            table: a dataset Table instance

        """
        if table_name in self.db.tables:
            self.db[table_name].drop()
        return self.db.create_table(table_name)

    def close(self):
        """Safely disconnect and release the SQLite file."""
        self.db.executable.close()
        self._db = None


class DBConnection(ContextDecorator):
    """Ensure the DBConnect connection is properly opened and closed."""

    def __init__(self, db_file):
        """Initialize context wrapper.

        Args:
            db_file: Path to the SQLite file

        """
        self.conn = None
        self.database_path = db_file

    def __enter__(self):
        """Connect to the database and return connection reference.

        Returns:
            dict: connection to sqlite database

        """
        self.conn = DBConnect(self.database_path)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection."""  # noqa: DAR101
        self.conn.close()


def rm_brs(line):
    """Replace all whitespace (line breaks, etc) with spaces."""  # noqa: DAR101,DAR201
    return ' '.join(line.split())


def uniq_table_id():
    """Return a unique table ID based on the current time in ms.

    Returns:
        str: in format `U<timestamp_ns>`

    """
    return f'U{time.time_ns()}'


def write_csv(csv_path, rows):
    """Write a csv file with appropriate line terminator and encoding.

    Args:
        csv_path: path to CSV file
        rows: list of lists to write to CSV file

    """
    with open(csv_path, 'w', newline='\n', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            writer.writerow(row)


def export_table_as_csv(csv_filename, table):
    """Create a CSV file summarizing a table of a `dataset` database.

    Args:
        csv_filename: Path to csv file
        table: table from dataset database

    """
    rows = [[*table.columns]]
    for row in table:
        rows.append([*row.values()])
    write_csv(csv_filename, rows)


def safe_col_name(args_pair):
    """Ensure that the column name is safe for SQL (unique value, no spaces, no trailing punctuation).

    Typically called with `df.columns = [*map(safe_col_name, enumerate(df.columns.to_list()))]`

    Args:
        args_pair: tuple of arguments from map function in `(idx, col)`

    Returns:
        string: safely formatted string for SQLite

    """
    idx, col = args_pair
    col = col.strip().replace(' ', '_').replace('.', '_').replace(',', '_')
    return str(idx) if col == '' else col


def store_reference_tables(db_file, data_dicts, meta_table_name=META_TABLE_NAME):
    """Store multi-dimensionsal data in a SQLite database.

    WARN: This will append to the META_TABLE_NAME without checking for duplicates. Handling de-duping separately

    Args:
        db_file: Path to a `.db` file
        data_dicts: all data to be stored in SQLite. Can contain Pandas dataframes
        meta_table_name: optional name of the main SQLite table. Default is `META_TABLE_NAME`

    """
    with DBConnection(db_file) as data_db:
        meta_table = []
        unique = uniq_table_id()
        for dict_idx, data_dict in enumerate(data_dicts):
            lookup = {}
            for key_idx, (key, value) in enumerate(data_dict.items()):
                if isinstance(value, pd.DataFrame):
                    table_name = f'{unique}D{dict_idx}K{key_idx}'
                    table = data_db.new_table(table_name)
                    value.columns = [*map(safe_col_name, enumerate(value.columns.to_list()))]
                    table.insert_many([*value.to_dict(orient='records')])
                    lookup[key] = table_name
                else:
                    lookup[key] = value
            meta_table.append(lookup)

        table_main = data_db.db.create_table(meta_table_name)
        table_main.insert_many(meta_table)


def get_table(db_file, table_name, drop_id_col=True):
    """Retrieve the meta table as a Pandas dataframe.

    Args:
        db_file: Path to a `.db` file
        table_name: SQLite table name
        drop_id_col: if True, drop the `id` column from SQL. Default is True

    Returns:
        df_table: pandas dataframe for the values in the specified table (`meta_table_name`)

    """
    with DBConnection(db_file) as data_db:
        df_table = pd.DataFrame([*data_db.db[table_name].all()])
    # Optionally remove the 'id' column added in the SQL database
    if drop_id_col:
        df_table = df_table.drop(['id'], axis=1)
    return df_table  # noqa: R504


# ----------------------------------------------------------------------------------------------------------------------
# General Helpers


def enable_verbose_pandas():
    """Update global pandas configuration for printed dataframes."""
    # Enable all columns to be displayed at once (or tweak to set a new limit)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    # Optionally modify number of rows shown
    pd.set_option('display.max_rows', None)


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
