"""Test dash_helpers."""

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
    fail_result = {'x': ['length of list should be 2, it is 3']}

    assert dash_helpers.validate(pass_doc_1, schema) == {}
    assert dash_helpers.validate(pass_doc_2, schema) == {}
    assert dash_helpers.validate(fail_doc_1, schema) == fail_result
