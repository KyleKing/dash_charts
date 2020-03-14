"""Helpers for building Dash applications."""

import argparse

from cerberus import Validator

# Plotly Colors:
# ['Blackbody', 'Blackbody_r', 'Bluered', 'Bluered_r', 'Blues', 'Blues_r', 'Cividis', 'Cividis_r', 'Earth', 'Earth_r',
#  'Electric', 'Electric_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'Hot', 'Hot_r', 'Jet', 'Jet_r', 'Picnic',
#  'Picnic_r', 'Portland', 'Portland_r', 'Rainbow', 'Rainbow_r', 'RdBu', 'RdBu_r', 'Reds', 'Reds_r', 'Viridis',
#  'Viridis_r', 'YlGnBu', 'YlGnBu_r', 'YlOrRd', 'YlOrRd_r', 'scale_name', 'scale_name_r', 'scale_pairs',
#  'scale_pairs_r', 'scale_sequence', 'scale_sequence_r']
# >>> plotly.colors.plotlyjs.Hot
# ['rgb(0,0,0)', 'rgb(230,0,0)', 'rgb(255,210,0)', 'rgb(255,255,255)']


def validate(document, schema, **validator_kwargs):
    """Validate a data structure. Return errors if any found.

    Cerberus Documentation: https://docs.python-cerberus.org/en/stable/validation-rules.html

    Args:
        document: data structure to validate
        schema: expected structure
        validator_kwargs: additional keyword arguments for Validator class

    Returns:
        list: validation errors

    """
    validator = Validator(schema, **validator_kwargs)
    validator.validate(document)
    return validator.errors


def parse_cli_port():
    """Configure the CLI options for Dash applications.

    Returns:
        int: port number

    """
    parser = argparse.ArgumentParser(description='Process Dash Parameters.')
    parser.add_argument('--port', type=int, default=8050,
                        help='Pass port number to Dash server. Default is 8050')
    args = parser.parse_args()
    return args.port


# Probably not possible to implement as a class
# TODO: Methods for convert df to json > dump to UI / load from UI > convert to DF
# class DataCache:
#
#     name = 'TODO-UniqueName'
#     element = (name, 'data')  # Use as input to state/input/output
#
#     def layout():
#         return ?
#
#     def write_df():
#         return {}
#
# Maybe just methods for formatting df as records for JSON, then methods for loading back to df?
