"""Helpers for building Dash applications."""

import argparse


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
