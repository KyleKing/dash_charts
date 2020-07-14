# FIXME: Need to generalize for non-URL. Should use 'identifier' column

"""Helpers for managing the JSON response cache to reduce load on API."""

import time
from pathlib import Path

from .dash_helpers import DBConnect, uniq_table_id, write_pretty_json

CACHE_DIR = Path(__file__).parent / 'local_cache'
"""Path to folder with all downloaded responses from Kitsu API."""

FILE_DATA = DBConnect(CACHE_DIR / '_file_lookup_database.db')
"""Global instance of the DBConnect() for the file lookup database."""


def initialize_cache():
    """Ensure that the directory and database exist. Remove files from database if manually removed."""
    table = FILE_DATA.db.create_table('files')

    removed_files = []
    for row in table:
        if not Path(row['filename']).is_file():
            removed_files.append(row['filename'])

    for filename in removed_files:
        table.delete(filename=filename)


def match_url_in_cache(url):
    """Return list of matches for the given URL in the file database.

    Args:
        url: full URL to use as a reference if already downloaded

    Returns:
        list: list of match object with keys of the SQL table

    """
    return [*FILE_DATA.db.load_table('files').find(url=url)]


def store_response(prefix, url, obj):
    """Store the response object as a JSON file and track in a SQLite database.

    Args:
        prefix: string used to create more recognizable filenames
        url: full URL to use as a reference if already downloaded
        obj: JSON object to write

    Raises:
        RuntimeError: if duplicate match found when storing

    """
    filename = CACHE_DIR / f'{prefix}_{uniq_table_id()}.json'
    new_row = {'filename': str(filename), 'url': url, 'timestamp': time.time()}
    # Check that the URL isn't already in the database
    matches = match_url_in_cache(url)
    if len(matches) > 0:
        raise RuntimeError(f'Already have an entry for this URL (`{url}`): {matches}')
    # Update the database and store the file
    FILE_DATA.db.load_table('files').insert(new_row)
    write_pretty_json(filename, obj)
