"""Test utils_data."""

import tempfile
from pathlib import Path
import pandas as pd

from dash_charts import utils_data


def test_enable_verbose_pandas():
    """Test enable_verbose_pandas."""
    pd.set_option('display.max_columns', 0)

    utils_data.enable_verbose_pandas()  # act

    pd.get_option('display.max_columns') is None


def test_validate():
    """Test the validate function."""
    schema = {
        'x': {
            'items': [{'type': ['integer', 'float']}, {'type': ['integer', 'float']}],
            'required': True,
            'type': 'list',
        },
        'y': {
            'items': [{'type': ['integer', 'float']}, {'type': ['integer', 'float']}],
            'required': False,
            'type': 'list',
        },
    }
    pass_doc_1 = {'x': [3, -4.0], 'y': [1e-6, 1e6]}
    pass_doc_2 = {'x': [-1e6, 1e6]}
    fail_doc_1 = {'x': [1, 2, 3]}

    fail_result = {'x': ['length of list should be 2, it is 3']}  # act

    assert utils_data.validate(pass_doc_1, schema) == {}
    assert utils_data.validate(pass_doc_2, schema) == {}
    assert utils_data.validate(fail_doc_1, schema) == fail_result


def test_json_dumps_compact():
    """Test json_dumps_compact."""
    result = utils_data.json_dumps_compact({'A': ['A1', 'A2', 'A3'], 'B': {'C': ['A']}})

    assert result == """{
    \"A\": [\"A1\",\"A2\",\"A3\"],
    \"B\": {
        \"C\": [
            \"A\"
        ]
    }
}"""


def test_write_pretty_json():
    """Test write_pretty_json."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        json_path = Path(tmp_dir) / 'tmp.json'
        utils_data.write_pretty_json(json_path, {'A': [1, 2, 3], 'B': 2})

        result = json_path.read_text()

    assert result == """{
    \"A\": [
        1,
        2,
        3
    ],
    \"B\": 2
}"""


def test_write_csv():
    """Test write_csv."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        csv_path = Path(tmp_dir) / 'tmp.json'
        utils_data.write_csv(csv_path, [['header 1', 'headder 2'], ['row 1', 'a'], ['row 2', 'b']])

        result = csv_path.read_text()

    assert result == 'header 1,headder 2\nrow 1,a\nrow 2,b\n'


def test_get_unix():
    """Test get_unix."""
    result = utils_data.get_unix('31Dec1999', '%d%b%Y')

    assert result == 946616400.0


def test_format_unix():
    """Test format_unix."""
    result = utils_data.format_unix(946616400, '%d%b%Y')

    assert result == '31Dec1999'


def test_uniq_table_id():
    """Test uniq_table_id."""
    result = utils_data.uniq_table_id()

    assert result.startswith('U')
    assert len(result) == 20


def test_list_sql_tables():
    """Test list_sql_tables."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir) / 'tmp.db'
        with utils_data.SQLConnection(db_path) as conn:
            # Create EVENTS table
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE EVENTS (
                id   INT   PRIMARY KEY   NOT NULL,
                label   TEXT   NOT NULL
            );""")
            cursor.execute("""CREATE TABLE MAIN (
                id   INT   PRIMARY KEY   NOT NULL,
                value   INT   NOT NULL
            );""")
            conn.commit()

        result = utils_data.list_sql_tables(db_path)

    assert result == ['EVENTS', 'MAIN']
