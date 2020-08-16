"""Test utils_data."""

import tempfile
from pathlib import Path

from dash_charts import utils_data
# def enable_verbose_pandas():
# import pandas as pd
# pd.get_option('display.max_columns')  is None
# def write_csv(csv_path, rows):
# def list_sql_tables(db_file):


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
        tmp_file = Path(tmp_dir) / 'tmp.json'
        utils_data.write_pretty_json(tmp_file, {'A': [1, 2, 3], 'B': 2})

        result = tmp_file.read_text()

    assert result == """{
    \"A\": [
        1,
        2,
        3
    ],
    \"B\": 2
}"""


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
