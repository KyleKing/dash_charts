"""Helpers for building Dash applications."""

import argparse


def rm_brs(line):
    """Replace all whitespace (line breaks, etc) with spaces."""  # noqa: DAR101,DAR201
    return ' '.join(line.split())


def parse_dash_cli_args():  # pragma: no cover
    """Configure the CLI options for Dash applications.

    Returns:
        dict: keyword arguments for Dash

    """
    parser = argparse.ArgumentParser(description='Process Dash Parameters.')
    parser.add_argument('--port', type=int, default=8050,
                        help='Pass port number to Dash server. Default is 8050')
    parser.add_argument('--nodebug', action='store_true', default=False,
                        help='If set, will disable debug mode. Default is to set `debug=True`')
    args = parser.parse_args()
    return {'port': args.port, 'debug': not args.nodebug}


def graph_return(resp, keys):
    """Based on concepts of GraphQL, return specified subset of response.

    Args:
        resp: dictionary with values from function
        keys: list of keynames from the resp dictionary

    Returns:
        the `resp` dictionary with only the keys specified in the `keys` list

    Raises:
        RuntimeError: if `keys` is not a list or tuple

    """
    if not (len(keys) and isinstance(keys, (list, tuple))):
        raise RuntimeError(f'Expected list of keys for: `{resp.items()}`, but received `{keys}`')
    ordered_responses = [resp.get(key, None) for key in keys]
    return ordered_responses if len(ordered_responses) > 1 else ordered_responses[0]
