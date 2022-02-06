"""Helpers for building Dash applications."""

import csv
import json
import sqlite3
import time
from contextlib import ContextDecorator
from datetime import datetime
from pathlib import Path

import pandas as pd
from cerberus import Validator

# ----------------------------------------------------------------------------------------------------------------------
# For Working with Data


def enable_verbose_pandas(max_columns=None, max_rows=None, max_seq_items=None):
    """Update global pandas configuration for printed dataframes.

    Args:
        max_columns: the number of max columns. Default is None (to show all)
        max_rows: the number of max rows. Default is None (to show all)
        max_seq_items: the number of max sequence items. Default is None (to show all) # TODO: what does this set?

    """
    # Enable all columns to be displayed at once (or tweak to set a new limit)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', max_columns)

    # Optionally modify number of rows shown
    pd.set_option('display.max_rows', max_rows)
    if max_seq_items:
        pd.options('display.max_seq_items', max_seq_items)


def append_df(df_old, df_new):
    """Handle appending a dataframe if the old_df is None. Useful for iteration.

    Args:
        df_old: dataframe or None
        df_new: new dataframe to append. Expects all columns to match

    Returns:
        dataframe: combined dataframe

    """
    return df_new if df_old is None else pd.concat([df_old, df_new]).reset_index(drop=True)


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


def json_dumps_compact(data):   # noqa: CCR001
    """Format provided dictionary into compact JSON. Lists will be in one line rather than split on new lines.

    Args:
        data: JSON-serializable dictionary

    Returns:
        str: JSON-formatted string with lists compacted into a single line

    """
    clean_data = {}
    # Check each key/value pair to determine if any intermediary strings are needed for later formatting
    for key, raw in data.items():
        # PLANNED: Convert to FP and recursive calls?
        if isinstance(raw, list):
            values = [f'``{value}``' if isinstance(value, str) else value for value in raw]
            clean_data[key] = '[' + ','.join(map(str, values)) + ']'
        else:
            clean_data[key] = raw
    # Format the dictionary into JSON and replace the special characters used as intermediaries
    raw_json = json.dumps(clean_data, indent=4, separators=(',', ': '), sort_keys=True)
    return (
        raw_json
        .replace(': "[', ': [')
        .replace(']"', ']')
        .replace('``', '"')
        .replace("'", '"')
    )


def write_pretty_json(filename, obj):
    """Write indented JSON file.

    Args:
        filename: Path or plain string filename to write (should end with `.json`)
        obj: JSON object to write

    """
    Path(filename).write_text(json.dumps(obj, indent=4, separators=(',', ': ')))


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


# ----------------------------------------------------------------------------------------------------------------------
# Time Helpers

US_TIME_FORMAT = '%m/%d/%Y %H:%M:%S'
"""String time format with month/year (MM/DD/YYYY HH:MM:SS)."""

DASHED_TIME_FORMAT_US = '%m-%d-%Y %H:%M:%S'
"""Dashed time format with month first (MM-DD-YYYY HH:MM:SS)."""

DASHED_TIME_FORMAT_YEAR = '%Y-%m-%d %H:%M:%S'
"""Dashed time format with year first (YYYY-MM-DD HH:MM:SS)."""

TIME_FORMAT_FILE = '%Y-%m-%d_%H%M%S'
"""Filename-safe time format with year first (YYYY-MM-DD_HHMMSS)."""

GDP_TIME_FORMAT = '%d%b%Y %H:%M:%S'
"""Good Documentation Practice time format (DDMMMYYYY HH:MM:SS)."""


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


# ----------------------------------------------------------------------------------------------------------------------
# General SQL


def uniq_table_id():
    """Return a unique table ID based on the current time in ms.

    Returns:
        str: in format `U<timestamp_ns>`

    """
    return f'U{time.time_ns()}'


# ----------------------------------------------------------------------------------------------------------------------
# sqlite3


class SQLConnection(ContextDecorator):
    """Ensure the SQLite connection is properly opened and closed."""

    def __init__(self, db_path):
        """Initialize context wrapper.

        Args:
            db_path: Path to a SQLite file

        """
        self.conn = None
        self.db_path = db_path

    def __enter__(self):
        """Connect to the database and return connection reference.

        Returns:
            dict: connection to sqlite database

        """
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection."""  # noqa: DAR101
        self.conn.close()


def list_sql_tables(db_path):
    """Return all table names from the SQL database.

    Args:
        db_path: path to SQLite database file

    Returns:
        list: of unique table names in the SQL database

    """
    with SQLConnection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE TYPE = "table"')
        return [names[0] for names in cursor.fetchall()]
