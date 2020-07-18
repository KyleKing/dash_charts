"""Helpers for managing a generic JSON data file cache. Could be used to reduce API calls, etc.

Notes on `dataset`. Full documentation: https://dataset.readthedocs.io/en/latest/api.html

```py
db = FILE_DATA.db
db.create_table('table_name', primary_id='slug', primary_type=db.types.text)
db.load_table('table_name')  # Fails if table does not exist

ic(db.tables, db['table_name'].columns, len(db['table_name']))
ic([*db['table_name'].all()][:2])

table = db['table_name']
# # Below snippets from Kitsu-Library-Availability
# ic([*table.find(id=[1, 3, 7])])
# ic([*table.find_one(id=4)])
# ic([*table.find(status='completed')])
# ic([*table.find(status={'<>': 'dropped'}, averageRating={'between': [60, 80]})])
# ic([*table.distinct('status')])
# # gt, >; || lt, <; || gte, >=; || lte, <=; || !=, <>, not; || between, ..

# Other:
table.update(dict(name='John Doe', age=47), ['name'])
```

"""

import json
import time
from pathlib import Path

from .dash_helpers import DBConnect, uniq_table_id, write_pretty_json

CACHE_DIR = Path(__file__).parent / 'local_cache'
"""Path to folder with all downloaded responses from Kitsu API."""

FILE_DATA = DBConnect(CACHE_DIR / '_file_lookup_database.db')
"""Global instance of the DBConnect() for the file lookup database."""


def get_files_table(db_instance=FILE_DATA):
    """Retrieved stored object from cache database.

    Args:
        db_instance: Connected Database file with `dash_helpers.DBConnect()`.

    Returns:
        table: Dataset table for the files lookup

    """
    return db_instance.db.load_table('files')


def initialize_cache(db_instance=FILE_DATA):
    """Ensure that the directory and database exist. Remove files from database if manually removed.

    Args:
        db_instance: Connected Database file with `dash_helpers.DBConnect()`.

    """
    table = db_instance.db.create_table('files')

    removed_files = []
    for row in table:
        if not Path(row['filename']).is_file():
            removed_files.append(row['filename'])

    for filename in removed_files:
        table.delete(filename=filename)


def match_identifier_in_cache(identifier, db_instance=FILE_DATA):
    """Return list of matches for the given identifier in the file database.

    Args:
        identifier: identifier to use as a reference if the corresponding data is already cached
        db_instance: Connected Database file with `dash_helpers.DBConnect()`.

    Returns:
        list: list of match object with keys of the SQL table

    """
    return [*get_files_table(db_instance).find(identifier=identifier)]


def store_cache_object(prefix, identifier, obj, db_instance=FILE_DATA):
    """Store the object as a JSON file and track in a SQLite database to prevent duplicates.

    Args:
        prefix: string used to create more recognizable filenames
        identifier: identifier to use as a reference if the corresponding data is already cached
        obj: JSON object to write
        db_instance: Connected Database file with `dash_helpers.DBConnect()`.

    Raises:
        RuntimeError: if duplicate match found when storing

    """
    # Check that the identifier isn't already in the database
    matches = match_identifier_in_cache(identifier, db_instance)
    if len(matches) > 0:
        raise RuntimeError(f'Already have an entry for this identifier (`{identifier}`): {matches}')
    # Update the database and store the file
    filename = CACHE_DIR / f'{prefix}_{uniq_table_id()}.json'
    new_row = {'filename': str(filename), 'identifier': identifier, 'timestamp': time.time()}
    get_files_table(db_instance).insert(new_row)
    write_pretty_json(filename, obj)


def retrieve_cache_object(identifier, db_instance=FILE_DATA):
    """Retrieved stored object from cache database.

    Args:
        identifier: identifier to use as a reference if the corresponding data is already cached
        db_instance: Connected Database file with `dash_helpers.DBConnect()`.

    Raises:
        RuntimeError: if not exactly one match found

    """
    matches = match_identifier_in_cache(identifier, db_instance)
    if len(matches) != 1:
        raise RuntimeError(f'Did not find exactly one entry for this identifier (`{identifier}`): {matches}')
    return json.loads(Path(matches[0]['filename']).read_text())
