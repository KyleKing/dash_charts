"""Test utils_cache."""

from dash_charts.dash_helpers import DBConnect
from dash_charts.utils_cache import (CACHE_DIR, get_files_table, initialize_cache, retrieve_cache_object,
                                     store_cache_object)


def test_utils_cache():
    """Test the utils_cache helper methods."""
    # Initialize and clear cache for the expected identifier
    test_db = DBConnect(CACHE_DIR / '_test_lookup.db')
    initialize_cache(test_db)
    identifier = 'Test'
    get_files_table(test_db).delete(identifier=identifier)
    # Save an object to the cache
    prefix = 'TestFile'
    obj = {'this_is_test': True}
    store_cache_object(prefix, identifier, obj, test_db)

    result = retrieve_cache_object(identifier, test_db)

    assert result == obj
