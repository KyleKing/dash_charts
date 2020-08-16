"""Test utils_dataset."""

import tempfile
from pathlib import Path

from dash_charts import utils_dataset


def test_db_connect():
    """Test DBConnect."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        database = utils_dataset.DBConnect(tmp_dir / 'tmp.db')
        table = database.db.create_table('test')
        csv_filename = tmp_dir / 'tmp.csv'
        table.insert({'username': 'username', 'value': 1})
        utils_dataset.export_table_as_csv(csv_filename, table)
        database.close()

        result = csv_filename.read_text()

    assert result == 'id,username,value\n1,username,1\n'
