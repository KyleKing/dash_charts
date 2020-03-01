"""Helpers for building Dash applications."""

import argparse

from cerberus import Validator


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
