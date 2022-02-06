"""Helpers for building Dash applications."""

from contextlib import ContextDecorator

import dataset
import pandas as pd

from .utils_data import SQLConnection, uniq_table_id, write_csv

# ----------------------------------------------------------------------------------------------------------------------
# dataset

META_TABLE_NAME = 'meta'
"""Name of the Meta-Data table in a typical SQLite database."""


class DBConnect:  # noqa: H601
    """Manage database connection since closing connection isn't possible."""

    db_path = None
    """Path to the local storage SQLite database file. Initialize in `__init__()`."""

    _db = None

    @property
    def db(self):
        """Return connection to database. Will create new connection if one does not exist already.

        Returns:
            dict: `dataset` database instance

        """
        if self._db is None:
            self._db = dataset.connect(f'sqlite:///{self.db_path}')
        return self._db

    def __init__(self, db_path):
        """Store the database path and ensure the parent directory exists.

        Args:
            db_path: Path to the SQLite file

        """
        self.db_path = db_path.resolve()
        self.db_path.parent.mkdir(exist_ok=True)
        self.db  # Check initial connection

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

    def __init__(self, db_path):
        """Initialize context wrapper.

        Args:
            db_path: Path to the SQLite file

        """
        self.conn = None
        self.db_path = db_path

    def __enter__(self):
        """Connect to the database and return connection reference.

        Returns:
            dict: connection to sqlite database

        """
        self.conn = DBConnect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection."""  # noqa: DAR101
        self.conn.close()


def export_table_as_csv(csv_filename, table):
    """Create a CSV file summarizing a table of a `dataset` database.

    Args:
        csv_filename: Path to csv file
        table: table from dataset database

    """
    rows = [[*table.columns]]
    rows.extend([*row.values()] for row in table)
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


def store_reference_tables(db_path, data_dicts, meta_table_name=META_TABLE_NAME, use_raw_sql=True):   # noqa: CCR001
    """Store multi-dimensionsal data in a SQLite database.

    WARN: This will append to the META_TABLE_NAME without checking for duplicates. Handling de-duping separately

    Args:
        db_path: Path to a `.db` file
        data_dicts: all data to be stored in SQLite. Can contain Pandas dataframes
        meta_table_name: optional name of the main SQLite table. Default is `META_TABLE_NAME`
        use_raw_sql: if True, will use the raw SQL connection rather than DataSet. This is faster for meta_tables that
            have more than 1000 rows, but less safe

    """
    with SQLConnection(db_path) as conn:
        meta_table = []
        unique = uniq_table_id()
        for dict_idx, data_dict in enumerate(data_dicts):
            lookup = {}
            for key_idx, (key, value) in enumerate(data_dict.items()):
                if isinstance(value, pd.DataFrame):
                    value.columns = [*map(safe_col_name, enumerate(value.columns.to_list()))]
                    table_name = f'{unique}Dict{dict_idx}Key{key_idx}'
                    value.to_sql(table_name, con=conn)
                    lookup[key] = table_name
                else:
                    lookup[key] = value
            meta_table.append(lookup)

    if use_raw_sql:
        add_meta_table_records_sql(db_path, meta_table, meta_table_name)
    else:
        with DBConnection(db_path) as data_db:
            table_main = data_db.db.create_table(meta_table_name)
            table_main.insert_many(meta_table)


def add_meta_table_records_sql(db_path, meta_table, meta_table_name):
    """Store new rows for the meta table using a more performant SQLite implementation.

    WARN: This will append to the META_TABLE_NAME without checking for duplicates. Handling de-duping separately

    Args:
        db_path: Path to a `.db` file
        meta_table: list of dictionaries to add to the meta_table
        meta_table_name: optional name of the main SQLite table

    """
    with SQLConnection(db_path) as conn:
        cursor = conn.cursor()
        keys = [*meta_table[0].keys()]
        names_formatted = ','.join(map(safe_col_name, enumerate(keys)))
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {meta_table_name}({names_formatted});')
        rows = [[row[col] for col in keys] for row in meta_table]
        places = ','.join(['?'] * len(keys))
        cursor.executemany(f'INSERT INTO {meta_table_name}({names_formatted}) VALUES ({places});', rows)
        conn.commit()


def get_table(db_path, table_name, drop_id_col=True):
    """Retrieve the meta table as a Pandas dataframe.

    Args:
        db_path: Path to a `.db` file
        table_name: SQLite table name
        drop_id_col: if True, drop the `id` column from SQL. Default is True

    Returns:
        df_table: pandas dataframe for the values in the specified table (`meta_table_name`)

    """
    with DBConnection(db_path) as data_db:
        df_table = pd.DataFrame([*data_db.db[table_name].all()])
    # Optionally remove the 'id' column added in the SQL database
    if drop_id_col:
        df_table = df_table.drop(labels=['id', 'index'], axis=1, errors='ignore')
    return df_table  # noqa: R504
