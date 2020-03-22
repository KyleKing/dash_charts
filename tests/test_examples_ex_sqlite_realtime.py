"""Test the file examples/ex_sqlite_realtime.py."""

import pytest

from .examples import ex_sqlite_realtime


@pytest.mark.CHROME
def test_smoke_test_ex_sqlite_realtime(dash_duo):
    dash_duo.start_server(ex_sqlite_realtime.app.app)

    import time
    time.sleep(1)

    assert not dash_duo.get_logs()
