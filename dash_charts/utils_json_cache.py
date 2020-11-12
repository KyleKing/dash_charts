"""Helpers for managing a generic JSON data file cache. Can be used to reduce API calls, etc.

Full dataset documentation: https://dataset.readthedocs.io/en/latest/api.html

"""

import json
import time
from pathlib import Path

from .utils_data import uniq_table_id, write_pretty_json
from .utils_dataset import DBConnect

#  FIXME: Add versioning to the cache directory with semver logic: https://pypi.org/project/semantic-version/

CACHE_DIR = Path(__file__).parent / 'local_cache'
"""Path to folder with all downloaded responses from Kitsu API."""

FILE_DATA = DBConnect(CACHE_DIR / '_file_lookup_database.db')
"""Global instance of the DBConnect() for the file lookup database."""

CACHE_TABLE_NAME = 'files'
"""Table name containing the cache file information."""

ID_KEY = 'identifier'
"""Name of the SQLite column containing the unique identifier."""
TS_KEY = 'timestamp'
"""Name of the SQLite column containing the timestamp."""
FILENAME_KEY = 'filename'
"""Name of the SQLite column containing the string filename."""

# TODO: Enable versioning of data and automatic deletion when the version changes
DATA_VERSION_KEY = 'data_version'
"""Key to indicate the data version."""


def get_files_table(db_instance):
    """Retrieve stored object from cache database.

    Args:
        db_instance: Connected Database file with `DBConnect()`.

    Returns:
        table: Dataset table for the files lookup

    """
    return db_instance.db.load_table(CACHE_TABLE_NAME)


def initialize_cache(db_instance):
    """Ensure that the directory and database exist. Remove files from database if manually removed.

    Args:
        db_instance: Connected Database file with `DBConnect()`.

    """
    table = db_instance.db.create_table(CACHE_TABLE_NAME)

    removed_files = []
    for row in table:
        if not Path(row[FILENAME_KEY]).is_file():
            removed_files.append(row[FILENAME_KEY])

    for filename in removed_files:
        table.delete(filename=filename)


def get_cache_dict(db_instance):
    """Return a dictionary `{identifier: path}` keys and values.

    Args:
        db_instance: Connected Database file with `DBConnect()`.

    Returns:
        dict: dictionary `{identifier: path}` keys and values

    """
    table = get_files_table(db_instance)
    return {row[ID_KEY]: Path(row[FILENAME_KEY]) for row in table}


def match_identifier_in_cache(identifier, db_instance):
    """Return list of matches for the given identifier in the file database.

    Args:
        identifier: identifier to use as a reference if the corresponding data is already cached
        db_instance: Connected Database file with `DBConnect()`.

    Returns:
        list: list of match object with keys of the SQL table

    """
    kwargs = {ID_KEY: identifier}
    return [*get_files_table(db_instance).find(**kwargs)]


def store_cache_as_file(prefix, identifier, db_instance, cache_dir=CACHE_DIR, suffix='.json'):
    """Store the reference in the cache database and return the file so the user can handle saving the file.

    Args:
        prefix: string used to create more recognizable filenames
        identifier: identifier to use as a reference if the corresponding data is already cached
        db_instance: Connected Database file with `DBConnect()`.
        cache_dir: path to the directory to store the file. Default is `CACHE_DIR
        suffix: string filename suffix. The default is `.json`

    Returns:
        Path: to the cached file. Caller needs to write to the file

    Raises:
        RuntimeError: if duplicate match found when storing

    """
    # Check that the identifier isn't already in the database
    matches = match_identifier_in_cache(identifier, db_instance)
    if matches:
        raise RuntimeError(f'Already have an entry for this identifier (`{identifier}`): {matches}')
    # Update the database and store the file
    filename = cache_dir / f'{prefix}_{uniq_table_id()}{suffix}'
    new_row = {FILENAME_KEY: str(filename), ID_KEY: identifier, TS_KEY: time.time()}
    get_files_table(db_instance).insert(new_row)
    return filename


def store_cache_object(prefix, identifier, obj, db_instance, cache_dir=CACHE_DIR):
    """Store the object as a JSON file and track in a SQLite database to prevent duplicates.

    Args:
        prefix: string used to create more recognizable filenames
        identifier: identifier to use as a reference if the corresponding data is already cached
        obj: JSON object to write
        db_instance: Connected Database file with `DBConnect()`.
        cache_dir: path to the directory to store the file. Default is `CACHE_DIR

    Raises:
        Exception: if duplicate match found when storing

    """
    filename = store_cache_as_file(prefix, identifier, db_instance, cache_dir)
    try:
        write_pretty_json(filename, obj)
    except Exception:
        # If writing the file fails, ensure that the record is removed from the database
        get_files_table(db_instance).delete(filename=filename)
        raise


def retrieve_cache_fn(identifier, db_instance):
    """Retrieve stored object from cache database.

    Args:
        identifier: identifier to use as a reference if the corresponding data is already cached
        db_instance: Connected Database file with `DBConnect()`.

    Returns:
        Path: to the cached file. Caller needs to read the file

    Raises:
        RuntimeError: if not exactly one match found

    """
    matches = match_identifier_in_cache(identifier, db_instance)
    if len(matches) != 1:
        raise RuntimeError(f'Did not find exactly one entry for this identifier (`{identifier}`): {matches}')
    return Path(matches[0][FILENAME_KEY])


def retrieve_cache_object(identifier, db_instance):
    """Retrieve stored object from cache database.

    Args:
        identifier: identifier to use as a reference if the corresponding data is already cached
        db_instance: Connected Database file with `DBConnect()`.

    Returns:
        dict: object stored in the cache

    """
    filename = retrieve_cache_fn(identifier, db_instance)
    return json.loads(filename.read_text())
