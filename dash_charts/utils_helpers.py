"""Helpers for building Dash applications."""

import argparse
import time
from datetime import datetime
from typing import Optional

from beartype import beartype

# ----------------------------------------------------------------------------------------------------------------------
# General Debug


@beartype
def debug_time(message: str, last: Optional[datetime] = None) -> datetime:
    """Debug timing issues.

    Args:
        message: string message to print
        last: last timestamp

    Returns:
        timestamp: the current timestamp to calculate the next delta

    """
    if last is None:
        last = time.time()
    now = time.time()
    delta = now - last
    if delta > 0.5:
        print(message, delta)  # noqa: T001
    return now


# ----------------------------------------------------------------------------------------------------------------------
# Dash Helpers


def parse_dash_cli_args():  # pragma: no cover
    """Configure the CLI options for Dash applications.

    Returns:
        dict: keyword arguments for Dash

    """
    parser = argparse.ArgumentParser(description='Process Dash Parameters.')
    parser.add_argument(
        '--port', type=int, default=8050,
        help='Pass port number to Dash server. Default is 8050',
    )
    parser.add_argument(
        '--nodebug', action='store_true', default=False,
        help='If set, will disable debug mode. Default is to set `debug=True`',
    )
    args = parser.parse_args()
    return {'port': args.port, 'debug': not args.nodebug}


# ----------------------------------------------------------------------------------------------------------------------
# Functional Programming


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
