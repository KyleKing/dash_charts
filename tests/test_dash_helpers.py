"""Test dash_helpers."""

import tempfile
from pathlib import Path

from dash_charts import dash_helpers


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

    assert dash_helpers.validate(pass_doc_1, schema) == {}
    assert dash_helpers.validate(pass_doc_2, schema) == {}
    assert dash_helpers.validate(fail_doc_1, schema) == fail_result


def test_json_dumps_compact():
    """Test json_dumps_compact."""
    result = dash_helpers.json_dumps_compact({'A': ['A1', 'A2', 'A3'], 'B': {'C': ['A']}})

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
        dash_helpers.write_pretty_json(tmp_file, {'A': [1, 2, 3], 'B': 2})

        result = tmp_file.read_text()

    assert result == """{
    \"A\": [
        1,
        2,
        3
    ],
    \"B\": 2
}"""


def test_db_connect():
    """Test DBConnect."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        database = dash_helpers.DBConnect(tmp_dir / 'tmp.db')
        table = database.db.create_table('test')
        csv_filename = tmp_dir / 'tmp.csv'
        table.insert({'username': 'username', 'value': 1})
        dash_helpers.export_table_as_csv(csv_filename, table)
        database.close()

        result = csv_filename.read_text()

    assert result == 'id,username,value\n1,username,1\n'


def test_rm_brs():
    """Test rm_brs."""
    result = dash_helpers.rm_brs("""Testing with line breaks.
\n\n\n\nShould make this\r\none\nline.""")

    assert result == 'Testing with line breaks. Should make this one line.'


def test_uniq_table_id():
    """Test uniq_table_id."""
    result = dash_helpers.uniq_table_id()

    assert result.startswith('U')
    assert len(result) == 20


def test_graph_return():
    """Test the graph return function."""
    raw_resp = {'A': 1, 'B': 2, 'C': None}
    exp_resp = [2, 1]

    result = dash_helpers.graph_return(raw_resp, keys=('B', 'A'))

    assert result == exp_resp


def test_get_unix():
    """Test get_unix."""
    result = dash_helpers.get_unix('31Dec1999', '%d%b%Y')

    assert result == 946616400.0


def test_format_unix():
    """Test format_unix."""
    result = dash_helpers.format_unix(946616400, '%d%b%Y')

    assert result == '31Dec1999'
