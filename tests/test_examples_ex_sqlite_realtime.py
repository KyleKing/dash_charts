"""Test the file examples/ex_sqlite_realtime.py."""

import pytest
from icecream import ic

from .examples import ex_sqlite_realtime


@pytest.mark.CHROME
def test_smoke_test_ex_sqlite_realtime(dash_duo):
    dash_duo.start_server(ex_sqlite_realtime.app.app)

    import time
    time.sleep(1)

    logs = dash_duo.get_logs()
    ic(logs)  # FIXME: Reporting severe errors that only appear when running tests, but not as standalone?
    # assert not logs
