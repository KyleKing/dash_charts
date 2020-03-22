"""Helpers for building Dash applications."""

import argparse
import sqlite3
import time
from contextlib import ContextDecorator

from cerberus import Validator

# Plotly Colors:
# ['Blackbody', 'Blackbody_r', 'Bluered', 'Bluered_r', 'Blues', 'Blues_r', 'Cividis', 'Cividis_r', 'Earth', 'Earth_r',
#  'Electric', 'Electric_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'Hot', 'Hot_r', 'Jet', 'Jet_r', 'Picnic',
#  'Picnic_r', 'Portland', 'Portland_r', 'Rainbow', 'Rainbow_r', 'RdBu', 'RdBu_r', 'Reds', 'Reds_r', 'Viridis',
#  'Viridis_r', 'YlGnBu', 'YlGnBu_r', 'YlOrRd', 'YlOrRd_r', 'scale_name', 'scale_name_r', 'scale_pairs',
#  'scale_pairs_r', 'scale_sequence', 'scale_sequence_r']
# >>> plotly.colors.plotlyjs.Hot
# ['rgb(0,0,0)', 'rgb(230,0,0)', 'rgb(255,210,0)', 'rgb(255,255,255)']


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


def uniq_table_id():
    """Return a unique table ID based on the current time in ms.

    Returns:
        str: in format `U<timestamp_ns>`

    """
    return f'U{time.time_ns()}'
