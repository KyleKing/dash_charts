"""Test the file examples/ex_gantt.py."""

import pytest

from .examples import ex_gantt


@pytest.mark.CHROME
def test_smoke_test_ex_gantt(dash_duo):
    dash_duo.start_server(ex_gantt.app.app)

    import time
    time.sleep(1)

    assert not dash_duo.get_logs()
