"""Test the file examples/ex_rolling_chart.py."""

import pytest

from .examples import ex_rolling_chart


@pytest.mark.CHROME
def test_smoke_test_ex_rolling_chart(dash_duo):
    dash_duo.start_server(ex_rolling_chart.app.app)

    import time
    time.sleep(1)

    assert not dash_duo.get_logs()
